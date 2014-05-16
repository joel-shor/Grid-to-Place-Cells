/* Contains the one method that calculates the final activity
 * after global inhibition. Called from inhibition.cpp,
 * which has the method that attaches the C++ code to
 * the Python code. */

#include <stdio.h>
#include <iostream>
using namespace std;

double *sort(double *Is, const int &num_Is){
	double *sorted_Is = new double[num_Is];

	for (int i=0; i<num_Is; i++)
		sorted_Is[i] = Is[i];

	return sorted_Is;
}

double sum(double *Is, const int &num_Is){
	double cur_sum = 0;
	for (int i=0;i<num_Is;i++){
		cur_sum += Is[i];
	}
	return cur_sum;
}

double* inhibMethod(double *Is, const int &num_Is,
		const double &f_I, const double &f_p, const double &thresh,
		double &inhib){
	/* This is called a lot. Make it tight.

		calc_inhib(Is, f_I, f_p,thresh)
		Is is a list of inputs to place cells.
		f_I is the inhibition strength.
		f_p is the firing strength
		thresh is the threshold for inhibition to kick in.

		Returns an array of final activities, along with
		the final value of the inhibition.
	*/
	double *sorted_Is = sort(Is, num_Is); // Return a new, sorted array
	double IPlusSum = sum(sorted_Is,num_Is);

	if (IPlusSum* f_p < thresh){
		inhib = 0;
	}
	else{
		for (int i=0; i<num_Is; i++){
			cout<<"IPluSSum is "<<IPlusSum<<endl;
			int NPlus = num_Is - i;
			inhib = f_I * ( (f_p*IPlusSum-thresh) / (1+ f_I* NPlus *f_p) );
			cout<< "Inhib is at: "<<inhib<<endl;
			if (sorted_Is[i] - inhib >= 0){
				cout << "The final number of NPlus: "<<NPlus<<endl;
				break;}
			IPlusSum -= sorted_Is[i];
		}
	}

	// Calculate the steady-state firing rate
	double *final_acts = new double[num_Is];
	for (int i=0; i<num_Is; i++){
		double cur_act = Is[i] - inhib;
		final_acts[i] = (cur_act > 0) ? f_p*cur_act : 0;
	}

	// Clean up
	delete sorted_Is;

	return final_acts;
}

int main(){
	double Is[3] = {2,2,3};
	const double *f_I, *f_p, *thresh;
	const double fi = 2, fp =3, thre=1;
	f_I = &fi; f_p = &fp; thresh = &thre;
	double inhib;
	double* final_acts = inhibMethod(Is,3,
								*f_I,*f_p,*thresh,
								inhib);

	for (int i=0; i<3; i++)
		cout<<final_acts[i]<<" ";
	cout<<endl;

	cout << "Final inhib: "<<inhib<<endl;

	delete final_acts;
	return 0;
}
