#include<iostream>
using namespace std;

int main() {
	int t[3]={0,0,0};
	cin >> t[0];
        do {
	  t[1]+=1;
	  t[2]+=t[1];
        } while (t[1]<t[0]);
	cout << t[2] << endl;
	return 0;
}
