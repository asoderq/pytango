/*******************************************************************************

   This file is part of PyTango, a python binding for Tango

   http://www.tango-controls.org/static/PyTango/latest/doc/html/index.html

   Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
   
   PyTango is free software: you can redistribute it and/or modify
   it under the terms of the GNU Lesser General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
   
   PyTango is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU Lesser General Public License for more details.
  
   You should have received a copy of the GNU Lesser General Public License
   along with PyTango.  If not, see <http://www.gnu.org/licenses/>.
   
*******************************************************************************/

// This header file is just some template functions moved apart from
// wattribute.cpp, and should only be included there.

#pragma once

#include "tango_numpy.h"

namespace PyWAttribute {

    template<long tangoTypeConst>
    void __get_write_value_array_numpy(Tango::WAttribute &att, boost::python::object* obj)
    {
        typedef typename TANGO_const2type(tangoTypeConst) TangoScalarType;

        const TangoScalarType *buffer;
        att.get_write_value(buffer);
        size_t length = att.get_write_value_length();

        // Copy buffer in a python raw buffer
        const char *original_ch_buffer = reinterpret_cast<const char *>(buffer);
        PyObject* str_guard = PyString_FromStringAndSize(original_ch_buffer, length*sizeof(TangoScalarType));

        if (!str_guard) {
            throw_error_already_set();
        }

        // Create a numpy object based on it...
        static const int typenum = TANGO_const2numpy(tangoTypeConst);
        npy_intp dims[2];
        int nd = 1;

        char* ch_buffer = PyString_AsString(str_guard);

        if (att.get_data_format() == Tango::IMAGE) {
            nd = 2;
            dims[1] = att.get_w_dim_x();
            dims[0] = att.get_w_dim_y();
        } else {
            nd = 1;
            dims[0] = att.get_w_dim_x();
        }

        PyObject* array = PyArray_SimpleNewFromData(nd, dims, typenum, ch_buffer);
        if (!array) {
            Py_XDECREF(str_guard);
            throw_error_already_set();
        }
        PyArray_BASE(array) = str_guard;
        *obj = boost::python::object(boost::python::handle<>(array));
    }
    
    template<>
    void __get_write_value_array_numpy<Tango::DEV_STRING>(Tango::WAttribute &att, boost::python::object* obj)
    {
        __get_write_value_array_lists<Tango::DEV_STRING>(att, obj);
    }

    template<>
    void __get_write_value_array_numpy<Tango::DEV_ENCODED>(Tango::WAttribute &att, boost::python::object* obj)
    {
        __get_write_value_array_lists<Tango::DEV_STRING>(att, obj);
    }
}