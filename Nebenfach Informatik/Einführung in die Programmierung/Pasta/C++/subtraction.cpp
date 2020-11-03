#include<iostream>
using namespace std;

int main() {
	int t[2]={0,0};
	cin >> t[0];
	cin >> t[1];
        cout << (t[1]>t[0]) << endl;
        if (!(t[1]>t[0])) {
	  t[0]-=t[1];
	  cout << t[0] << endl;
        }
	return 0;
}
