#include <stdio.h>

#include <string.h>

#include <math.h>

#include <stdlib.h>
#include <dirent.h>



const int max_size=2000;

const int N=40;

const int max_w=50;



int main(int argc, char **argv)

{

    // declarations

    FILE *wordProjections, *questions, *answers,  *output;

    int numberOfWords, size, a, b, c, d, vA, vB, vC, vD, missing = 0;

    char stA[max_size], stB[max_size], stC[max_size], stD[max_size], file_name[max_size], questions_file_name[max_size], answers_file_name[max_size], output_file_name[max_size];
    char tempC[max_size], tempD[max_size];

    float *M, *y;

    char *vocab;

    float len, dist, temp;

  
    // argument handling

    if (argc<4) {

        printf("Usage: ./dist <PROJECTIONS> <QUESTIONS> <ANSWERS> <OUTPUT> \nwhere PROJECTIONS contains word projections, QUESTIONS contains questions and ANSWERS contains answers and OUTPUT contains the output file\n");

        return 0;

    }
    
    strcpy(file_name, argv[1]);

    strcpy(questions_file_name, argv[2]); 
    strcpy(answers_file_name, argv[3]); 
    strcpy(output_file_name, argv[4]); 
    

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
	if (counterQuestions >= 5 && (counterQuestions <= 6 || (counterQuestions <= 8 && line != "")))
	{
		if(counterQuestions == 5) { strcpy(FirstQuestion, line); } 
		if(counterQuestions == 6) { strcpy(SecondQuestion, line); } 
		if(counterQuestions == 7) { strcpy(ThirdQuestion, line); } 
		if(counterQuestions == 8) { strcpy(FourthQuestion, line); } 
	}
	
	if(counterQuestions >= 7) { break; }
    }
    fclose(questions);

    char str[max_size];
    char *ptr;
    strcpy (str, FirstQuestion);
    strtok_r (str, ":", &ptr);
    ptr[strlen(ptr)-1]='\0';
    
    float resultsFirstQuestion[100], resultsSecondQuestion[100], resultsThirdQuestion[100], resultsFourthQuestion[100], resultsAverage[100];
    char resultsC[100][max_size], resultsD[100][max_size];
    int NoOfAddedResults = 0, NoOfAddedResultsSecondQuestion = 0, NoOfAddedResultsThirdQuestion = 0, NoOfAddedResultsFourthQuestion = 0,
	NoOfResultsC = 0, NoOfResultsD = 0;
    
    while(fscanf(answers, "%s", &stC) != EOF)
    {
 	counterAnswers++;
	

        char *res = stC;
	res++[strlen(res)-1] = 0;
	
	char ans[max_size];
    	char *ans2;
    	strcpy (ans, res);
    	strtok_r (ans, ":", &ans2);
    	ptr[strlen(ans2)-1]='\0';
	strcpy(stC, ans);
	strcpy(stD, ans2);

	strcpy(resultsC[NoOfResultsC], stC); 
	NoOfResultsC++;
	strcpy(resultsD[NoOfResultsD], stD); 
	NoOfResultsD++;

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
        if(vC == numberOfWords || vD == numberOfWords) { continue; }
   
        int MissingAB = 0;
	
	//FirstQuestion
	if(strlen(FirstQuestion) != 0)
	{
		char str[max_size];
    		char *ptr;
    		strcpy (str, FirstQuestion);
    		strtok_r (str, ":", &ptr);
    		ptr[strlen(ptr)-1]='\0';
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


		if (vA == numberOfWords || vB == numberOfWords || vC == numberOfWords || vD == numberOfWords)

		{
		    MissingAB++;



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
		    for (a=0; a<size; a++) 
                    {			
			dist+=y[a]*M[a+vD*size];
		    }
		    
		    resultsFirstQuestion[NoOfAddedResults] = dist;
                    NoOfAddedResults = NoOfAddedResults + 1;
		  	     }
	}
         
	//SecondQuestion
	if(strlen(SecondQuestion) != 0)
	{
		char str[max_size];
    		char *ptr;
    		strcpy (str, SecondQuestion);
    		strtok_r (str, ":", &ptr);
    		ptr[strlen(ptr)-1]='\0';
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

		
		if (vA == numberOfWords || vB == numberOfWords || vC == numberOfWords || vD == numberOfWords)

		{
		    MissingAB++;



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
		    for (a=0; a<size; a++) 
                    {			
			dist+=y[a]*M[a+vD*size];
		    }
		    
		    resultsSecondQuestion[NoOfAddedResultsSecondQuestion] = dist;
                    NoOfAddedResultsSecondQuestion = NoOfAddedResultsSecondQuestion + 1;
		    
	     }
	

	}

	//Third Question
	if(strlen(ThirdQuestion) != 0)
	{
		char str[max_size];
    		char *ptr;
    		strcpy (str, ThirdQuestion);
    		strtok_r (str, ":", &ptr);
    		ptr[strlen(ptr)-1]='\0';
		strcpy(stA, str);
		strcpy(stB, ptr);


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

		if (vA == numberOfWords || vB == numberOfWords || vC == numberOfWords || vD == numberOfWords)

		{
		    MissingAB++;

		

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
		    for (a=0; a<size; a++) 
                    {			
			dist+=y[a]*M[a+vD*size];
		    }
		    
		    resultsThirdQuestion[NoOfAddedResultsThirdQuestion] = dist;
                    NoOfAddedResultsThirdQuestion = NoOfAddedResultsThirdQuestion + 1;
		    
	     }
	

	}

	// Fourth Question
	if(strlen(FourthQuestion) != 0)
	{
		char str[max_size];
    		char *ptr;
    		strcpy (str, ThirdQuestion);
    		strtok_r (str, ":", &ptr);
    		ptr[strlen(ptr)-1]='\0';
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

		if (vA == numberOfWords || vB == numberOfWords || vC == numberOfWords || vD == numberOfWords)

		{
		    MissingAB++;

		

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
		    for (a=0; a<size; a++) 
                    {			
			dist+=y[a]*M[a+vD*size];
		    }
		    
		    resultsFourthQuestion[NoOfAddedResultsFourthQuestion] = dist;
                    NoOfAddedResultsFourthQuestion = NoOfAddedResultsFourthQuestion + 1;
		  
	     }

	}

	int totalQuestions = 3 - MissingAB;
	if(NoOfAddedResultsFourthQuestion > 0) { totalQuestions = 4 - MissingAB; }
	
	for(a = 0; a < NoOfAddedResults; a++){
		if (totalQuestions == 3) { resultsAverage[a] = (resultsFirstQuestion[a] + resultsSecondQuestion[a] + resultsThirdQuestion[a])/totalQuestions; }
		else { resultsAverage[a] = (resultsFirstQuestion[a] + resultsSecondQuestion[a] + resultsThirdQuestion[a] + resultsFourthQuestion[a])/totalQuestions; }
	}


    } 

    // sort semantic similarity scores descending
    for(a = 0; a < NoOfAddedResults; a++)
    {
        for(b = a; b < NoOfAddedResults; b++)
        {
            if(resultsAverage[a] < resultsAverage[b]){
                temp = resultsAverage[a];
		strcpy(tempC, resultsC[a]);
                strcpy(tempD, resultsD[a]);
                resultsAverage[a] = resultsAverage[b];
                strcpy(resultsC[a], resultsC[b]);
                strcpy(resultsD[a], resultsD[b]);
                resultsAverage[b] = temp;
                strcpy(resultsC[b], tempC);
                strcpy(resultsD[b], tempD);
            }
        }
    }

    for(a = 0; a < NoOfAddedResults; a++){
		fprintf(output, "%f", resultsAverage[a]);
		fprintf(output, "%s", " ");
		fprintf(output, "%s", resultsC[a]);
		fprintf(output, "%s", ":");
                fprintf(output, "%s", resultsD[a]);
		fprintf(output, "%s", "\n");
	}

    fclose(answers);
    fclose(output);

    

    

    return 0;

}
