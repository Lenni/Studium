#include <iostream>
#include <vector>
#include <chrono>
#include <random>
#include <math.h>

using namespace std;

vector<int> make_array(int min, int max, int size);
vector<int> sort_array(vector<int> A, int range);
vector<int> shift_array(vector<int> A, int distance);

bool verify(vector<int> A, vector<int>B);

void print_array(vector<int> A);

int main(int argc, char** argv)
{
    int size;

    int min = -1000;
    int max = 1000;

    if(argc != 1)
    {
        size = atoi(argv[1]);
    }else
    {
        size = 1000;
    }

    for(; size > 0; size --)
    {
        vector<int> A = make_array(min, max, size);

        vector<int> A_s = shift_array(A, -min);
        vector<int> sorted_s = sort_array(A_s,(abs(min) + abs(max)));

        vector<int> sorted = shift_array(sorted_s, min);



        if(size > 5000 || size < 20)
        {
            print_array(A);
            cout << endl << endl;
            print_array(sorted);
            break;
        }

        bool result = verify(A, sorted);

        cout << endl << size << ": " << result << endl;
        if(!result) break;
    }

    return 0;
}

vector<int> make_array(int min, int max, int size)
{
    unsigned seed = chrono::system_clock::now().time_since_epoch().count();
    default_random_engine gen(seed);
    uniform_int_distribution<int> rand(min, max);

    vector<int> a;

    for(int i = 0; i < size; i++)
    {
        a.push_back(rand(gen));
    }

    return a;
}

vector<int> sort_array(vector<int> A, int range)
{
    vector<int> helper;
    vector<int> sorted;

    for(int i = 0; i <= range; i++)
    {
        helper.push_back(0);
    }

    for(int j = 0; j < A.size(); j++)
    {
        helper[A[j]]++;
    }

    for(int k = 0; k < helper.size(); k++)
    {
        if(helper[k] != 0)
        {
          for(int l = 0; l < helper[k]; l++)
          {
             sorted.push_back(k);
          }
        }
    }

    return sorted;
}

vector<int> shift_array(vector<int> A, int distance)
{
    for(int i = 0; i < A.size(); i++)
    {
        A[i] = A[i] + distance;
    }

    return A;
}

bool verify(vector<int> A, vector<int> B)
{
    int same = 0;

    if(A.size() != B.size())
    {
        cout << "Arrays not same Size!" << endl;
        cout << A.size() << "   " << B.size() << endl;
        //return false;
    }

    for(int i = 0; i < A.size(); i++)
    {
        bool found = false;
        for(int j = 0; j < B.size(); j++)
        {
            if(A[i] == B[j])
            {
                //cout << A[i] << "   " << B[j] << endl;
                same ++;
                found = true;
                break;
            }
        }
        if(!found)
        {
            cout << A[i] << endl;
        }
    }
    if(same != A.size())
    {
        return false;
    }else
    {
        return true;
    }
}

void print_array(vector<int> A)
{
    for(int i = 0; i < A.size(); i++)
    {
        cout << A[i] << endl;
    }
    return;
}

