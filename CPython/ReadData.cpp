#include <stdio.h>
#include <string.h>
#define CODE_SIZE 7

/*

g++ ReadData.cpp -o ReadData.o -std=c++11
*/

struct SimpleQuotaData
{
    char code[7];
    double last_pr;
    double b1_pr;
    double s1_pr;
    SimpleQuotaData* next;
};

SimpleQuotaData* ReadData(const char* filename)
{
    FILE* fp = fopen(filename, "r");
    if (fp == nullptr)
        perror("error in open file\n");
    char line[1024];
    SimpleQuotaData head{}, *temp{&head};
    head.next = nullptr;
    while( fgets(line, 1024, fp))
    {   
        SimpleQuotaData* new_data = new SimpleQuotaData;
        strncpy(new_data->code, line, CODE_SIZE);
        new_data->code[CODE_SIZE - 1] = 0;
        int read_n = sscanf(line+7, "%lf,%lf,%lf", &(new_data->last_pr), &(new_data->b1_pr), &(new_data->s1_pr));
        // printf("read %s: %s,%.2lf,%.2lf,%.2lf\n", line, new_data->code, new_data->last_pr, new_data->b1_pr, new_data->s1_pr);
        temp->next = new_data;
        temp = new_data;
        new_data->next = nullptr;
    }
    fclose(fp);
    return head.next;
}

int main()
{
    const SimpleQuotaData *pData, *temp;
    pData = ReadData("MarketData");
    temp = pData;
    while (temp != nullptr)
    {
        printf("%s,%.2lf,%.2lf,%.2lf\n", temp->code, temp->last_pr, temp->b1_pr, temp->s1_pr);
        temp = temp->next;
    }
    return 0;
}