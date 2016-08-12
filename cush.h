#pragma once
#include <vector>
#include "boost_for_export.h"
using namespace std;
void export_ImpactResult();
void export_Sim();
class ImpactResult {
public:
    double foo;
    vector<double> times;
    vector<double> pressures;
    vector<double> depths;
    vector<double> velocities; 
};
