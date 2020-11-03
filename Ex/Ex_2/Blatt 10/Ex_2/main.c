#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

typedef int bool;
#define true 1
#define false 0

#define VELOCITY false
#define POSITION true

#define ULTRA 0.00001
#define HIGH 0.0001
#define NORMAL 0.001
#define LOW 0.005

//Helper function to concat Strings in C

char* concat(const char *s1, const char *s2)
{
    char *result = malloc(strlen(s1)+strlen(s2)+1);
    strcpy(result, s1);
    strcat(result, s2);
    return result;
}

//Declaration of Simulaton Structs

struct particle;
struct box;
struct system;
struct vec3;

// Vector 3 Struct for Vector Properties of Objects

struct vec3{
  double x;
  double y;
  double z;
};

struct particle{
  char* name;
  struct vec3 position;
  struct vec3 velocity;
};

struct box{
  struct vec3 dimensions;
  char* name;

  struct particle part;
  struct vec3 expansion;
};


struct system{
  int time;
  bool readiness;
  int partno;
  struct box world;
};

//Constructor Functions to initialize the Different Structs

struct vec3 vec3(double x, double y, double z);
struct box box(char* name, struct vec3 dimensions, struct particle part, struct vec3 expansion);
struct particle particle(char* name, struct vec3 velocity, struct vec3 position);
struct system _system(int time, struct box world);

//Simulation Functions

void modify_world(struct system sys, struct vec3 dimensions);
struct particle modify_particle(struct particle part, struct vec3 data, bool mode);
void simulate_enviroment(struct system sys, struct particle part, int _time, double resolution);

int main(int argc, char** argv)
{
  /// Cerate Simulaton Enviroment and Particles
  struct vec3 vel1 = vec3(1000, 0, 0);
  struct vec3 pos1 = vec3(0, 0.5, 0);
  struct vec3 dim1 = vec3(1, 1, 1);
  struct vec3 expan = vec3(0.1, 0, 0);

  struct particle part1 = particle("Partikel 1", vel1, pos1);
  struct box world = box("Welt 1", dim1, part1, expan);
  struct system sys = _system(0, world);

  char* input = "a";
  printf("Start\n");

  // Check if an Argument was given
 if(argc == 2)
 {
   ///Run with Argument as Simulaton Stepsize
   simulate_enviroment(sys, part1, 0, atof(argv[1]));
 }else
 {
   ///Run with predefined Macro as Simulaton Stepsize
   simulate_enviroment(sys, part1, 0, ULTRA);
 }
  return 0;
}

//Vector 3 Constructor

struct vec3 vec3(double x, double y, double z)
{
  struct vec3 vector;

  vector.x = x;
  vector.y = y;
  vector.z = z;

  return vector;
}

//Epanding Box Constructor

struct box box(char* name, struct vec3 dimensions, struct particle part, struct vec3 expansion)
{
  struct box world;

  printf("Start Constructor!");
  world.expansion = expansion;
  world.dimensions.x = dimensions.x;
  world.dimensions.y = dimensions.y;
  world.dimensions.z = dimensions.z;
  world.name = name;

  world.part = part;

  printf("%s", concat(concat("Created Wold named: ", world.name), "\n"));

  return world;
}

//Gas Particle Constructor

struct particle particle(char* name, struct vec3 velocity, struct vec3 position)
{
  struct particle part;

  part.name = name;
  part.velocity = velocity;
  part.position = position;

  printf("Created Particle with Name: %s  Velo: %f  Pos: %f", part.name, part.velocity.x, part.position.x);

  return part;
}

//Simulation System Constructor

struct system _system(int time, struct box world)
{
  struct system sys;

  sys.time = time;
  sys.partno = 0;
  sys.world = world;
  sys.readiness = true;

  return sys;
}

//Interface Function to handle Box Expansion

void modify_world(struct system sys, struct vec3 dimensions)
{
  sys.world.dimensions.x = dimensions.x;
  sys.world.dimensions.y = dimensions.y;
  sys.world.dimensions.z = dimensions.z;
}

//Interface Funtion to handle Particle modifications

struct particle modify_particle(struct particle part, struct vec3 data, bool mode)
{
  if(mode == VELOCITY)
  {
    printf("\n Old Velocity: %f  New Velocity: %f   |v|: %f \n\n", part.velocity.x, data.x, fabs(part.velocity.x)+fabs(data.x));
    part.velocity = data;
  }else if(mode == POSITION)
  {
    part.position = data;
    //printf("Position Modified! \n");
  }

  return part;
}

//Main Simulation

void simulate_enviroment(struct system sys, struct particle part, int _time, double resolution)
{
  //Declare and Define Simulation properties
  double time = _time;
  double length = 1;
  double time_to_hit = 0;
  double hits = 0;
  bool print_stats = false;

  //Calculate Time to Hit Wall
  time_to_hit = (2*sys.world.dimensions.x)/part.velocity.x;

  //Run Simulation until Box has been fully Expanded
  while(sys.world.dimensions.x < 2)
  {
      struct vec3 pos = part.position;
      struct vec3 vel = part.velocity;
      pos.x = pos.x + vel.x * resolution;
      pos.y = pos.y + vel.y * resolution;
      pos.z = pos.z + vel.z * resolution;

      sys.world.dimensions.x = sys.world.dimensions.x + sys.world.expansion.x * resolution;
      sys.world.dimensions.y = sys.world.dimensions.y + sys.world.expansion.y * resolution;
      sys.world.dimensions.z = sys.world.dimensions.z + sys.world.expansion.z * resolution;


      if(pos.x >= sys.world.dimensions.x)
      {
          vel.x = -vel.x + 2*sys.world.expansion.x;
          hits++;
          print_stats = true;
          printf("\nHit X! \n\n");
          part = modify_particle(part, vel, VELOCITY);
      }else if(pos.y >= sys.world.dimensions.y)
      {
          vel.y = -vel.y + 2*sys.world.expansion.y;
          hits++;
          print_stats = true;
          printf("\nHit Y! \n\n");
          part = modify_particle(part, vel, VELOCITY);
      }else if(pos.z >= sys.world.dimensions.z)
      {
          vel.z = -vel.z + 2*sys.world.expansion.z;
          hits++;
          print_stats = true;
          printf("\nHit Z! \n\n");
          part = modify_particle(part, vel, VELOCITY);
      }else if(pos.x < 0)
      {
          vel.x = -vel.x;
          hits++;
          print_stats = true;
          printf("\nHit X! \n\n");
          part = modify_particle(part, vel, VELOCITY);
      }else if(pos.y < 0)
      {
          vel.y = -vel.y;
          hits++;
          print_stats = true;
          printf("Hit Y! \n\n");
          part = modify_particle(part, vel, VELOCITY);
      }else if(pos.z < 0)
      {
          vel.z = -vel.z;
          hits++;
          print_stats = true;
          printf("\n Hit Z! \n\n");
          part = modify_particle(part, vel, VELOCITY);
      }
      part = modify_particle(part, pos, POSITION);

      //Print Particle Information when a Wall has been Hit

      if(print_stats == true)
      {
        print_stats = false;

        printf("X: %f     %f", pos.x, sys.world.dimensions.x);
        printf("  Y: %f     %f", pos.y, sys.world.dimensions.y);
        printf("  Z: %f     %f \n", pos.z, sys.world.dimensions.z);
        printf("Time to Hit: %f s\n", fabs(time_to_hit));
      }

      time = time + resolution;
      time_to_hit = (2*sys.world.dimensions.x)/part.velocity.x;
  }

  //Print final Statistics

  printf("\n\n\n");
  printf("Expansion Time: %f s \n", time);
  printf("Final Length: %f m \n", sys.world.dimensions.x);
  printf("Final particle velocity |v|: %f m/s \n", abs(part.velocity.x));
  printf("Number of total Collisions: %f \n \r", hits);
}
