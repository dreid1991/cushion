#include "boost_stls.h"

void export_stls() {
    class_<std::vector<double> >("vecdouble")
        .def(vector_indexing_suite<std::vector<double> >() )
        ;
    class_<std::vector<std::vector<double> > >("vecdoubledouble")
        .def(vector_indexing_suite<std::vector<std::vector<double> > >() )
        ;
    class_<std::vector<int> >("vecInt")
        .def(vector_indexing_suite<std::vector<int> >() )
        ;

}
