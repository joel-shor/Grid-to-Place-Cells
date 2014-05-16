#include <Python.h>
#include <inhibMethod.cpp>

static PyObject * calc_inhibition(PyObject *self, PyObject *args)
{
	/* Connects C++ code to Python code by parsing in inputs
	 * and formatting them for output
    */
    PyObject * ListObj;

    const double *f_I, *f_p, *thresh;
    int numLines;

    if (!PyArg_ParseTuple(args, "0!ddd", &PyList_Type, &ListObj, &f_I, &f_p, &thresh))
        return NULL;

    /* get the number of lines passed to us */
    numLines = PyList_Size(ListObj);
    if (numLines < 0)   return NULL; /* Not a list */

    double Is[] = new double[numLines];
    PyObj * dbObj;
    for (i=0;i<numLines;i++){
    	dbObj = PyList_GetItem(listObj, i); /* Can't fail */
    	Is[i] = PyString_AsDouble( strObj );
    }

    /* Do the computation */
    double final_inhib;
    double *final_acts = inhibMethod(Is, numLines,
    						*f_I, *f_p, *thresh,
    						final_inhib);

    /* Perform formatting for output */
    // need to convert final_acts
    // need to convert final_inhib

    /* Clean up */
    delete Is;
    delete final_acts;

    return Py_BuildValue("i", sts);
}

static PyMethodDef SpamMethods[] = {
    {"calc_inhib",  calc_inhibition, METH_VARARGS,
     "Determine the inhibition."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
initspam(void)
{
    (void) Py_InitModule("spam", SpamMethods);
}
