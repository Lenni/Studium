#include<iostream>
using namespace std;

int main() {
	int t[3]={0,0,0};
	cin >> t[0];
	cin >> t[1];
        do {
	  t[2]+=t[0];
	  t[1]-=1;;
        } while (t[1]>0);
	cout << t[2] << endl;
	return 0;
}
