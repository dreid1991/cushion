#include "Python.h"
#include <boost/python.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/python/args.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/operators.hpp>

using namespace boost::python;
#include <tuple>
#include "boost_stls.h"
using namespace std;
#include "cush.h"
//#include "FixForceTwo.h"
BOOST_PYTHON_MODULE(Cush) {
    export_stls();
    export_Sim();
    export_ImpactResult();
}
