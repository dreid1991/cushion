#include <vector>
#include <string>
#include <cmath>
using namespace std;
//ALL UNITS ARE SI UNLESS OTHERWISE STATED
//Imp -> Impactor
const double R = 8.314;
const double pAtm = 101325;





double calcVolDot(double velImp, double massImp, double press, double area, double dt, double *velNext) {
    double deltaVel = (press - pAtm) * area / massImp * dt;
  //  printf("deltaVel %f press pressAtm %f %f\n", deltaVel, press, pAtm);
    velImp -= deltaVel;
    *velNext = velImp; 
    return -velImp * area;
}

double calcNDot(double press, double temp, vector<double> &holeSizes) {
    double molPerVolume = press / (R * temp);
    double massPerMol = 0.028 * .79 + 0.032 * .21; //79% N2, 21% O2
    double massPerVol = molPerVolume * massPerMol;

    double gasVel = sqrt(2/massPerVol * (press - pAtm));
    double nDot = 0;
    for (double holeSize : holeSizes) {
        nDot += holeSize * gasVel * molPerVolume;
    }
    return -nDot;
}


ImpactResult runSimulation(double velImpInit, double massImp, double tempInit, double volInit, double area, double pressInit, vector<double> holeSizes, double dt) {
    double moles = pressInit * volInit / (R * tempInit);
    double press = pressInit;
    double temp = tempInit;
    vector<double> temps(holeSizes.size(), tempInit);
    double velImp = velImpInit;
    double velImpNext = velImp;
    double vol = volInit;
    double engOnImp;
    ImpactResult res;
    double time = 0;
    auto appendData = [&] () {
        res.times.push_back(time);
        res.pressures.push_back(press);
        res.depths.push_back(volInit/area - vol/area);
        res.velocities.push_back(velImp);
    };
    appendData();
    int i=0;
    printf("time vol vel press moles engOnImp\n");
    while (velImpNext > .0001*velImpInit and vol > 0 and 1000 > time) {
        //printf("NEW TURN\n");
        double volDot = calcVolDot(velImp, massImp, press, area, dt, &velImpNext);
       // printf("volDot is %f\n", volDot);
        double molesDot = calcNDot(press, temp, holeSizes);
        double pressDot = molesDot * R * temp / vol - moles * R * temp * volDot / (vol * vol);

        engOnImp += (press-pAtm) * area * velImp * dt;
        velImp = velImpNext;

        vol += volDot * dt;
        press += pressDot * dt;
        moles += molesDot * dt;
        time += dt;
        appendData();
        i++;
    }
    printf("%f %f %f %f %f %f\n", time, vol, velImp, press, moles, engOnImp);
    return res;
}


int main() {
    double velImpInit = 2; //m/s
    double massImp = 1; //kg
    double tempInit = 300; //consider adding work done on sys later
    double volInit = .1; //1m^3, quite big
    double area = 1; //1m^2, so just looking at a cube
    double pressInit = 101325; //atmospheric in pascals
    vector<double> holeSizes;// = {0.01};
    holeSizes.push_back(0.006);
    /*
    holeSizes.push_back(0.001);
    holeSizes.push_back(0.001);
    holeSizes.push_back(0.001);
    holeSizes.push_back(0.001);
    holeSizes.push_back(0.001);
    */
    double dt = 0.0000001; //seconds
    ImpactResult res = runSimulation(velImpInit, massImp, tempInit, volInit, area, pressInit, holeSizes, dt);
    



    return 0;
}
