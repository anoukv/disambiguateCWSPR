#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

const int max_size=2000;
const int N=40;
const int max_w=50;

int main(int argc, char **argv)
{
    // declarations
    FILE *wordProjections, *questions, *output;
    int numberOfWords, size, counter, a, b, c, vA, vB, vC, missing;
    char stA[max_size], stB[max_size], stC[max_size], bestWord[max_size], file_name[max_size], questions_file_name[max_size], output_file_name[max_size];
    float *M, *y;
    char *vocab, *notFoundMessage;
    float bestDistance, len, dist;
    
    notFoundMessage = "NOTHING";

    // argument handling
    if (argc<4) {
        printf("Usage: ./dist <PROJECTIONS> <QUESTIONS> <OUTPUT> \nwhere PROJECTIONS contains word projections, QUESTIONS contains questions and OUTPUT contains the outpute file\n");
        return 0;
    }
    
    strcpy(file_name, argv[1]);
    strcpy(questions_file_name, argv[2]);
    strcpy(output_file_name, argv[3]);
    
    wordProjections=fopen(file_name, "rb");
    if (wordProjections==NULL)
    {
        printf("Projections file not found\n");
        return -1;
    }
    
    // get the number of words and number of dimensions (size)
    fscanf(wordProjections, "%d", &numberOfWords);
    fscanf(wordProjections, "%d", &size);
    
    // allocate memory for the vocabulary, matrix and y
    vocab=(char *)malloc(numberOfWords*max_w*sizeof(char));
    M=(float *)malloc(numberOfWords*size*sizeof(float));
    y=(float *)malloc(size*sizeof(float));
    
    if (M==NULL)
    {
        printf("Cannot allocate memory: %d MB\n", numberOfWords*size*sizeof(float)/1048576);
        return -1;
    }
    
    // fill the vocabulary and the matrix with normalized vectors
    for (b=0; b<numberOfWords; b++)
    {
        fscanf(wordProjections, "%s", &vocab[b*max_w]);
        for (a=0; a<size; a++)
        {
            fscanf(wordProjections, "%f", &M[a+b*size]);
        }
        
        len=0;
        for (a=0; a<size; a++)
        {
            len+=M[a+b*size]*M[a+b*size];
        }
        
        len=sqrt(len);
        for (a=0; a<size; a++)
        {
            M[a+b*size]/=len;
        }
    }
    
    // make whole vocabulary uppercase
    for (a=0; a<numberOfWords*max_w; a++)
    {
        vocab[a]=toupper(vocab[a]);
    }
    
    fclose(wordProjections);
    
    // open file with questions
    questions=fopen(questions_file_name, "rb");
    if (questions==NULL)
    {
        printf("Questions file not found\n");
        return -1;
    }
    
    // open file for output
    output = fopen(output_file_name, "w");
    
    // init counter
    counter = 0;
    missing = 0;
    
    // as long as we have not reached the EOF, look for answer to the question
    
    while(fscanf(questions,"%s", &stA) != EOF)
    {
        counter++;
        printf("%d\n", counter);
        fscanf(questions,"%s", &stB);
        fscanf(questions,"%s", &stC);
        
        // uppercase the words
        for (a=0; a<strlen(stA); a++)
        {
            stA[a]=toupper(stA[a]);
        }
        for (a=0; a<strlen(stB); a++)
        {
            stB[a]=toupper(stB[a]);
        }
        for (a=0; a<strlen(stC); a++)
        {
            stC[a]=toupper(stC[a]);
        }
        
        for (vA=0; vA<numberOfWords; vA++){
            if (!strcmp(&vocab[vA*max_w], stA))
            {
                break;
            }
        }
        for (vB=0; vB<numberOfWords; vB++)
        {
            if (!strcmp(&vocab[vB*max_w], stB))
            {
                break;
            }
        }
        for (vC=0; vC<numberOfWords; vC++)
        {
            if (!strcmp(&vocab[vC*max_w], stC))
            {
                break;
            }
        }
        
        if (vA == numberOfWords || vB == numberOfWords || vC == numberOfWords)
        {
//            printf("Word was not found in dictionary\n");
            fwrite(notFoundMessage, sizeof(char), strlen(notFoundMessage), output);
            fwrite("\n", sizeof(char), 1, output);
            missing++;

        }
        else
        {
            // compute y
            for (a=0; a<size; a++)
            {
                y[a] = M[a+vB*size]-M[a+vA*size] + M[a+ vC *size];
            }

            // normalize y again.
            len=0;
            for (a=0; a<size; a++)
            {
                len+=y[a]*y[a];
            }
            
            len=sqrt(len);
            for (a=0; a<size; a++)
            {
                y[a]/=len;
            }
            
            bestDistance = 0;
            
            // find best match to y
            for (c=0; c<numberOfWords; c++)
            {
                if(c != vC && c != vA && c != vB)
                {
                    dist=0;
                    for (a=0; a<size; a++)
                    {
                        dist+=y[a]*M[a+c*size];
                    }
                    if(dist > bestDistance)
                    {
                        bestDistance = dist;
                        strcpy(bestWord, &vocab[c*max_w]);
                    }
                }
                
            }
        }
        fwrite(bestWord, sizeof(char), strlen(bestWord), output);
        fwrite("\n", sizeof(char), 1, output);
    }
    
    fclose(questions);
    fclose(output);
    printf("From %d questions, %d were not answered properly. Keep this in mind.\nDone!", counter, missing);
    
    
    return 0;
}
