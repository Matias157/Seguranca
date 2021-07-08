#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unac.h>

#define CHAR_SPACE_LENGTH 62
char char_space[CHAR_SPACE_LENGTH] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

char* unidecode(char *inputStr) {
    char* out = 0;
    size_t out_length = 0;

    if(unac_string("UTF-8", inputStr, strlen(inputStr), &out, &out_length)) {
        perror("unac_string");
    } 
    else {
        return(out);
    }
}

char* caesarCipher(char *filename, int key) {
    char *buffer = 0;
    char *answer = 0;
    int length;
    FILE *f = fopen(filename, "rb");

    if(f) {
        fseek(f, 0, SEEK_END);
        length = ftell(f);
        fseek(f, 0, SEEK_SET);
        buffer = malloc(length);
        answer = malloc(length);
        if(buffer) {
            fread(buffer, 1, length, f);
        }
        fclose(f);
    }
    else {
        printf("Can't open file!\n");
        return(NULL);
    }

    buffer = unidecode(buffer);
    if(buffer) {
        int i, j;
        for(i = 0; i < strlen(buffer); i++) {
            for(j = 0; j < CHAR_SPACE_LENGTH; j++) {
                if(buffer[i] == char_space[j]) {
                    break;
                }
            }
            if(buffer[i] == char_space[j]) {
                answer[i] = char_space[(j + key) % CHAR_SPACE_LENGTH];
            }
            else {
                if(buffer[i] == ' ' || buffer[i] == '\n' || buffer[i] == '.' || buffer[i] == ',' || buffer[i] == '?') {
                    answer[i] = buffer[i];
                }
            }
        }
    }

    free(buffer);
    return(answer);
}

char* caesarDecipher(char *filename, int key) {
    char *buffer = 0;
    char *answer = 0;
    int length;
    FILE *f = fopen(filename, "rb");

    if(f) {
        fseek(f, 0, SEEK_END);
        length = ftell(f);
        fseek(f, 0, SEEK_SET);
        buffer = malloc(length);
        answer = malloc(length);
        if(buffer) {
            fread(buffer, 1, length, f);
        }
        fclose(f);
    }
    else {
        printf("Can't open file!\n");
        return(NULL);
    }
    
    if(buffer) {
        int i, j;
        for(i = 0; i < length; i++) {
            for(j = 0; j < CHAR_SPACE_LENGTH; j++) {
                if(buffer[i] == char_space[j]) {
                    break;
                }
            }
            if(buffer[i] == char_space[j]) {
                if(((j - key) % CHAR_SPACE_LENGTH) < 0) {
                    answer[i] = char_space[CHAR_SPACE_LENGTH + ((j - key) % CHAR_SPACE_LENGTH)];
                }
                else {
                    answer[i] = char_space[(j - key) % CHAR_SPACE_LENGTH];
                }
            }
            else {
                if(buffer[i] == ' ' || buffer[i] == '\n' || buffer[i] == '.' || buffer[i] == ',' || buffer[i] == '?') {
                    answer[i] = buffer[i];
                }
            }
        }
    }

    free(buffer);
    return(answer);
}

int freqAnal(char *filename) {
    char *buffer = 0;
    int frequencies[CHAR_SPACE_LENGTH] = {0};
    int key = 0;
    int keyindex = 0;
    int length;
    FILE *f = fopen(filename, "rb");

    if(f) {
        fseek(f, 0, SEEK_END);
        length = ftell(f);
        fseek(f, 0, SEEK_SET);
        buffer = malloc(length);
        if(buffer) {
            fread(buffer, 1, length, f);
        }
        fclose(f);
    }
    else {
        printf("Can't open file!\n");
        return(0);
    }

    buffer = unidecode(buffer);
    if(buffer) {
        int i, j;
        for(i = 0; i < strlen(buffer) - 1; i++) {
            for(j = 0; j < CHAR_SPACE_LENGTH; j++) {
                if(buffer[i] == char_space[j]) {
                    frequencies[j]++;
                    break;
                }
            }
        }
    }

    free(buffer);

    int j = 0;
    for(j = 0; j < CHAR_SPACE_LENGTH; j++) {
        if(frequencies[j] > key) {
            key = frequencies[j];
            keyindex = j;
        }
    }

    key = ((keyindex - 26) % CHAR_SPACE_LENGTH);

    return(key);
}

char* vernamCipher(char *filename, char *key) {
    char *file_buffer = 0;
    char *key_buffer = 0;
    char *answer = 0;
    int length;
    FILE *f = fopen(filename, "rb");
    FILE *fk = fopen(key, "rb");

    if(f) {
        fseek(f, 0, SEEK_END);
        length = ftell(f);
        fseek(f, 0, SEEK_SET);
        file_buffer = malloc(length);
        answer = malloc(length);
        if(file_buffer) {
            fread(file_buffer, 1, length, f);
        }
        fclose(f);
    }
    else {
        printf("Can't open file!\n");
        return(NULL);
    }

    if(fk) {
        fseek(fk, 0, SEEK_END);
        length = ftell(fk);
        fseek(fk, 0, SEEK_SET);
        key_buffer = malloc(length);
        if(key_buffer) {
            fread(key_buffer, 1, length, fk);
        }
        fclose(fk);
    }
    else {
        printf("Can't open file!\n");
        return(NULL);
    }

    file_buffer = unidecode(file_buffer);

    if(file_buffer && key_buffer) {
        int i, j, k;
        for(i = 0; i < strlen(file_buffer); i++) {
            for(j = 0; j < CHAR_SPACE_LENGTH; j++) {
                if(file_buffer[i] == char_space[j]) {
                    break;
                }
            }
            for(k = 0; k < CHAR_SPACE_LENGTH; k++) {
                if(key_buffer[i] == char_space[k]) {
                    break;
                }
            }
            if(file_buffer[i] == char_space[j] && key_buffer[i] == char_space[k]) {
                answer[i] = char_space[(j + k) % CHAR_SPACE_LENGTH];
            }
            else {
                if(file_buffer[i] == ' ' || file_buffer[i] == '\n' || file_buffer[i] == '.' || file_buffer[i] == ',' || file_buffer[i] == '?') {
                    answer[i] = file_buffer[i];
                }
            }
        }
    }

    free(file_buffer);
    free(key_buffer);
    return(answer);
}

char* vernamDecipher(char *filename, char *key) {
    char *file_buffer = 0;
    char *key_buffer = 0;
    char *answer = 0;
    int length;
    FILE *f = fopen(filename, "rb");
    FILE *fk = fopen(key, "rb");

    if(f) {
        fseek(f, 0, SEEK_END);
        length = ftell(f);
        fseek(f, 0, SEEK_SET);
        file_buffer = malloc(length);
        answer = malloc(length);
        if(file_buffer) {
            fread(file_buffer, 1, length, f);
        }
        fclose(f);
    }
    else {
        printf("Can't open file!\n");
        return(NULL);
    }

    if(fk) {
        fseek(fk, 0, SEEK_END);
        length = ftell(fk);
        fseek(fk, 0, SEEK_SET);
        key_buffer = malloc(length);
        if(key_buffer) {
            fread(key_buffer, 1, length, fk);
        }
        fclose(fk);
    }
    else {
        printf("Can't open file!\n");
        return(NULL);
    }

    if(file_buffer && key_buffer) {
        int i, j, k;
        for(i = 0; i < length; i++) {
            for(j = 0; j < CHAR_SPACE_LENGTH; j++) {
                if(file_buffer[i] == char_space[j]) {
                    break;
                }
            }
            for(k = 0; k < CHAR_SPACE_LENGTH; k++) {
                if(key_buffer[i] == char_space[k]) {
                    break;
                }
            }
            if(file_buffer[i] == char_space[j] && key_buffer[i] == char_space[k]) {
                if(((j - k) % CHAR_SPACE_LENGTH) < 0) {
                    answer[i] = char_space[CHAR_SPACE_LENGTH + ((j - k) % CHAR_SPACE_LENGTH)];
                }
                else {
                    answer[i] = char_space[(j - k) % CHAR_SPACE_LENGTH];
                }
            }
            else {
                if(file_buffer[i] == ' ' || file_buffer[i] == '\n' || file_buffer[i] == '.' || file_buffer[i] == ',' || file_buffer[i] == '?') {
                    answer[i] = file_buffer[i];
                }
            }
        }
    }

    free(file_buffer);
    free(key_buffer);
    return(answer);
}

int main(int argc, char *argv[]) {
    if(!strcmp(argv[1], "cesar")) {
        if(argc != 7) {
            printf("Invalid parameters!\n");
            return(-1);
        }
        else {
            if(!strcmp(argv[2], "-c")) {
                char *output = caesarCipher(argv[5], strtol(argv[4], NULL, 10));
                FILE *fp = fopen(argv[6], "w");
                fprintf(fp, "%s", output);
                fclose(fp);
                free(output);
                return(0);
            }
            else if(!strcmp(argv[2], "-d")) {
                char *output = caesarDecipher(argv[5], strtol(argv[4], NULL, 10));
                FILE *fp = fopen(argv[6], "w");
                fprintf(fp, "%s", output);
                fclose(fp);
                free(output);
                return(0);
            }
        }
    }
    else if(!strcmp(argv[1], "analFreq")) {
        int key = freqAnal(argv[2]);
        printf("Chave encontrada!!!\n   --- k = %d ---", key);
        return(0);
    }
    else if(!strcmp(argv[1], "vernam")) {
        if(argc != 6) {
            printf("Invalid parameters!\n");
            return(-1);
        }
        else {
            if(!strcmp(argv[2], "-c")) {
                char *output = vernamCipher(argv[4], argv[3]);
                FILE *fp = fopen(argv[5], "w");
                fprintf(fp, "%s", output);
                fclose(fp);
                free(output);
                return(0);
            }
            else if(!strcmp(argv[2], "-d")) {
                char *output = vernamDecipher(argv[4], argv[3]);
                FILE *fp = fopen(argv[5], "w");
                fprintf(fp, "%s", output);
                fclose(fp);
                free(output);
                return(0);
            }
        }
    }
    printf("Invalid parameters!\n");
    return(-1);
}