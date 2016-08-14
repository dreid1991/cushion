#pragma once
#include <vector>
#include "boost_for_export.h"
using namespace std;
void export_ImpactResult();
void export_Sim();
class ImpactResult {
public:
    vector<double> times;
    vector<double> pressures;
    vector<double> depths;
    vector<double> velocities; 
    vector<double> molesTotal;
    double avgPressure;
    double stdevPressure;
    bool failed;
};
