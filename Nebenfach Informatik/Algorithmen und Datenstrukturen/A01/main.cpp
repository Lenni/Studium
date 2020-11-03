#include <iostream>
#include <chrono>
#include <cstdlib>
#include <string>
#include <cmath>

using namespace std;

int* make_array(int size);
int search_upper(int* array, int size, int r);
int search_lower(int* array, int size, int r);

void print(int* array, int size);


int main(int argc, char** argv)
{
  int size;
  int r, l;
  int rindex, lindex;

  if(argc == 2)
  {
    size = atoi(argv[1]);
  }else
  {
    cout << "Wie groß soll das zu durchsuchende Array sein? " << endl;
     cin >> size;
  }

  int* array = make_array(size);

  print(array, size);

  cout << "Was soll die linke Zahl sein? " << endl;
  cin >> l;
  cout << "Was soll die rechte Zahl sein? " << endl;
  cin >> r;

  rindex = search_upper(array, size, r);
  lindex = search_lower(array, size, l);

  int count = rindex - lindex + 1;

  cout << "Es befinden sich " << count << " Zahlen im Intervall [" << l << "," << r << "]"<< endl;

}


int* make_array(int size)
{
  int* array = (int*) malloc(size * sizeof(int));
  int num = 0;

  srand(time(NULL));

  for(int i = 0; i < size; i++)
  {
    num += (rand()%10);
    array[i] = num;
  }

  return array;
}

void print(int* array, int size)
{
  for(int i = 0; i < size; i++)
  {

    cout << i << "  " << array[i] << endl;
  }
}

int search_lower(int* array, int size, int r)
{
  int upper_bound, lower_bound;

  upper_bound = size;
  lower_bound = 0;

  if(r <= array[0])
  {
    return 0;
  }else if( r > array[size-1])
  {
    return size;
  }else
  {
    while(upper_bound != lower_bound)
    {
      int median = floor((upper_bound + lower_bound) / 2.0);

      if(r > array[median])
      {
        lower_bound = median + 1;
      }
      else
      {
        upper_bound = median;
      }
    }
    return upper_bound;
  }
}

int search_upper(int* array, int size, int l)
{
  int upper_bound, lower_bound;

  upper_bound = size;
  lower_bound = 0;

  if(l < array[0])
  {
    return -1;
  }else if(l > array[size-1])
  {
    return size-1;
  }else
  {
    while(upper_bound != lower_bound)
    {
      int median = ceil((upper_bound + lower_bound) / 2.0);

      if(l < array[median])
      {
        upper_bound = median - 1;
      }
      else
      {
        lower_bound = median;
      }
    }
    return upper_bound;
  }
}
