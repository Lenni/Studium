#include <iostream>
#include <math.h>
#include <vector>

#define C_E0 8.85*pow(10, -12)
#define PI 3.1415
#define C_SIGMA 1

using namespace std;

double distance(vector<double> dist);
double field(float d, int N, float l);

int main()
{
    for(float d = 0.1; d <= 10; d *= 10)
    {
        cout << "Feld von d = " << d << "   N=11, l=1:   " << field(d, 11, 1) << endl;
        cout << "Feld von d = " << d << "   N=101, l=0.1:   " << field(d, 101, 0.1) << endl;
        cout << "Feld von d = " << d << "   N=1001, l=0.1:      " << field(d, 1001, 0.1) << endl;
    }

    return 0;
}

double field(float d, int N, float l)
{
    double strength = 0;

    double Q = (C_SIGMA*pow((N-1), 2)*pow(l, 2))/pow(N, 2);

    //cout << "Q: " << Q << endl;

    for(int i = -(N-1)/2; i <= (N-1)/2; i++)
    {
        for(int j = -(N-1)/2; j <= (N-1)/2; j++)
        {
            vector<double> dists;
            dists.push_back(d);
            dists.push_back(i*l);
            dists.push_back(j*l);

            strength += d*Q/(pow(distance(dists), 3)*(4*PI*C_E0));

            //cout <<"Distance: " << distance(dists) << endl;
            //cout << "Strength: " << Q/(distance(dists)) << endl;
            //cout << "Field: " << strength << endl;

        }
    }

    return strength;
}


double distance(vector<double> dist)
{
    double sum = 0;

    for(int i = 0; i < dist.size(); i++)
    {
        sum += pow(dist.at(i), 2);
    }

    return sqrt(sum);
}
