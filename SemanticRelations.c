#include <stdio.h>
#include <string.h>
#include <math.h>
#include <malloc.h>

const int max_size=2000;
const int N=40;
const int max_w=50;

int main(int argc, char **argv)
{
    // declarations
    FILE *wordProjections, *questions, *answers,  *output;
    int numberOfWords, size, a, b, c, d, vA, vB, vC, vD, missing = 0;
    char stA[max_size], stB[max_size], stC[max_size], stD[max_size], file_name[max_size], questions_file_name[max_size], answers_file_name[max_size], output_file_name[max_size];
    float *M, *y;
    char *vocab, *notFoundMessage;
    float len, dist;
    
    notFoundMessage = "NOTHING";

    // argument handling
    if (argc<4) {
        printf("Usage: ./dist <PROJECTIONS> <QUESTIONS> <ANSWERS> <OUTPUT> \nwhere PROJECTIONS contains word projections, QUESTIONS contains questions and ANSWERS contains answers and OUTPUT contains the outpute file\n");
        return 0;
    }
    
    strcpy(file_name, argv[1]);
    strcpy(questions_file_name, argv[2]);
    strcpy(answers_file_name, argv[3]);
    strcpy(output_file_name, argv[4]);

    //FILE *output = fopen (output_file_name, "wb");
    
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

    // open file with answers
    answers=fopen(answers_file_name, "rb");
    if (answers == NULL)
    {
	printf("Questions file not found\n");
        return -1;
    }
    
    // open file for output
    output = fopen(output_file_name, "w");
    
    // init counter
    int counterAnswers = 0, counterQuestions = 0;
    char FirstQuestion[max_size], SecondQuestion[max_size], ThirdQuestion[max_size], FourthQuestion[max_size], line[max_size];
    
    while ( fgets (line, sizeof line, questions) != NULL ) /* read a line */
    {
	counterQuestions++;
	printf("%d\n", counterQuestions);
	if (counterQuestions >= 5 && (counterQuestions <= 6 || (counterQuestions <= 8 && line != "")))
	{
		if(counterQuestions == 5) { strcpy(FirstQuestion, line); } 
		if(counterQuestions == 6) { strcpy(SecondQuestion, line); } 
		if(counterQuestions == 7) { strcpy(ThirdQuestion, line); } 
		if(counterQuestions == 8) { strcpy(FourthQuestion, line); } 
		/*switch(counterQuestions):
		{
			case 4:
				strcpy(FirstQuestion, line);
				break;
			case 5:
				strcpy(SecondQuestion, line);
				break;
			case 6:
				strcpy(ThirdQuestion, line);
				break;
			default:
				strcpy(FourthQuestion, line;
				break;
		}*/
	}
	
	if(counterQuestions >= 7) { break; }
    }
    fclose(questions);

    char str[max_size];
    char *ptr;
    strcpy (str, FirstQuestion);
    strtok_r (str, ":", &ptr);
    ptr[strlen(ptr)-1]='\0';
    printf ("'%s'  '%s'\n", str, ptr);

    /*char *firstToken, *secondToken;
    firstToken = strtok(FirstQuestion, ":");
    secondToken = strtok(FirstQuestion, ":");
    secondToken = strtok(NULL, ":");
    printf("First question is %s with A %s and B %s\n", FirstQuestion, firstToken, secondToken);*/
    printf("First question is %s\n", FirstQuestion);
    printf("Second question is %s\n", SecondQuestion);
    printf("Third question is %s\n", ThirdQuestion);
    printf("Fourth question is %s\n", FourthQuestion);
    if(strlen(FourthQuestion) == 0) { printf("is empty");} else {printf("is not empty");}

    // as long as we have not reached the answer file EOF, look at each answer
    while(fscanf(answers, "%s", &stC) != EOF)
    {
 	counterAnswers++;
	printf("%d\n", counterAnswers);
	printf("%s\n", stC);
	// for each answer compute the similary score with each word relation pair for the current relation inside the questions file
	//char mystr[] = "Nmy stringP";
	//char *p = mystr;
        char *res = stC;
	res++[strlen(res)-1] = 0;
	
	char ans[max_size];
    	char *ans2;
    	strcpy (ans, res);
    	strtok_r (ans, ":", &ans2);
    	ptr[strlen(ans2)-1]='\0';
    	printf ("Answer tokens are %s and %s \n", ans, ans2);
	strcpy(stC, ans);
	strcpy(stD, ans2);
	//printf ("Final answer tokens are %s and %s \n", stC, stD);

	for (a=0; a<strlen(stC); a++)
        {
            stC[a]=toupper(stC[a]);
        }
	for (a=0; a<strlen(stD); a++)
        {
            stD[a]=toupper(stD[a]);
        }
	
	for (vC=0; vC<numberOfWords; vC++)
        {
            if (!strcmp(&vocab[vC*max_w], stC))
            {
                break;
            }
        }
	for (vD=0; vD<numberOfWords; vD++)
        {
            if (!strcmp(&vocab[vD*max_w], stD))
            {
                break;
            }
        }

	if(strlen(FirstQuestion) != 0)
	{
		char str[max_size];
    		char *ptr;
    		strcpy (str, FirstQuestion);
    		strtok_r (str, ":", &ptr);
    		ptr[strlen(ptr)-1]='\0';
    		printf ("|%s| |%s|", str, ptr);
		
		/*char ansA[max_size];
    		char *ansA2;
    		strcpy (ansA, FirstQuestion);
    		strtok_r (ansA, ":", &ansA2);
    		ptr[strlen(ansA2)-1]='\0';*/
    		//printf ("First question tokens are |%s| and |%s| \n", str, ptr);
		strcpy(stA, str);
		strcpy(stB, ptr);

		// uppercase the words
		for (a=0; a<strlen(stA); a++)
		{
		    stA[a]=toupper(stA[a]);
		}
		for (a=0; a<strlen(stB); a++)
		{
		    stB[a]=toupper(stB[a]);
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

		printf ("A is %s B is %s C is %s D is %s\n", stA, stB, stC, stD);
		printf("vA:%d vB:%d vC:%d and vD:%d", vA, vB, vC, vD);
		if (vA == numberOfWords || vB == numberOfWords || vC == numberOfWords || vD == numberOfWords)
		{
		    printf("Word was not found in dictionary %d vA:%d and A is %s vB:%d and B is %s vC:%d and C is %s vD:%d and D is %s\n", numberOfWords, vA, stA, vB, stB, vC, stC, vD, stD);
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

		    // compute the cosine similarity between y and D
		    dist = 0;
		    for (c=0; c<numberOfWords; c++) 
		    {
			if(c != vA && c != vB && c != vC && c!= vD)
                	{
				for (a=0; a<size; a++) 
				{
					//dist+=M[a+b*size]*M[a+c*size];
					dist+=y[a]*M[a+c*size];
				}
			}
		    }
		    
                    printf("distance is: %d", dist);
		    fprintf(output, "%f", &dist);
		    fprintf(output, "%s", " ");
		    fprintf(output, "%s", stC);
		    fprintf(output, "%s", ":");
                    fprintf(output, "%s", stD);
		    fprintf(output, "%s", "\n");
	     }
	}

    } 

    fclose(answers);
    fclose(output);
    //printf("From %d questions, %d were not answered properly. Keep this in mind.\nDone!", counter, missing);
    
    return 0;
}
