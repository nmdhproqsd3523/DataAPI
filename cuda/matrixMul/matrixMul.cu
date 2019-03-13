// https://www.jianshu.com/p/a0184e73a460

#include "cuda_runtime.h"
#include "device_launch_parameters.h"
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <math.h>

#define w 2000

struct Matrix
{
    int width;
    int height;
    float *elements;
};

__device__ float getElement(Matrix *A, int row, int col)
{
    return A->elements[row * A->width + col];
}

__device__ void setElement(Matrix *A, int row, int col, float value)
{
    A->elements[row * A->width + col] = value;
}

__global__ void matMulKernel(Matrix *A, Matrix *B, Matrix *C)
{
    float Cvalue = 0.0;
    int row = threadIdx.y + blockIdx.y * blockDim.y;
    int col = threadIdx.x + blockIdx.x * blockDim.x;
	//int tid = threadIdx.x;
    for (int i = 0; i < A->width; ++i)
    {
        int index = (int)getElement(B, i, col) % 23;
        Cvalue += getElement(A, row, i) * getElement(B, i, col);
        // Cvalue += Cvalue / (double)3.1;
        //sudo /usr/local/cuda-10.2/bin/nvprof --metrics branch_efficiency  ./matrixMul
        //if (index == 17)
        //{
        //    for (int i = 0; i < 23; i++)
        //    {
        //        //Cvalue += Cvalue / (double)3.1;
        //    }
        //}
        Cvalue += Cvalue / (double)0.3456789;
        //Cvalue += Cvalue / (float)3.123234;
        //else
        //{
            //Cvalue += Cvalue / (double)3.2;
        //}
        //Cvalue += Cvalue / (double)3.22;
        //Cvalue += Cvalue / (double)3.23;
        //Cvalue += Cvalue / (float)3.1;
        

        //printf("%f \n", rsqrtf(4));
        //Cvalue += sqrtf(Cvalue);
        //Cvalue += acosf(Cvalue);
        //if (index == 0)
        {
            //Cvalue += sqrtf(Cvalue);
            //Cvalue += Cvalue / (double)3.1;
        }
        /*
        else if (index == 1)
        {
            Cvalue += Cvalue / (double)3.1415926;
        }
        else if (index == 2)
        {
            Cvalue += Cvalue / (double)2.71828;
        }
        else if (index == 3)
        {
            Cvalue += Cvalue / (double)1.4141;
        }
        else if (index == 4)
        {
            Cvalue += Cvalue / (double)1.4142;
        }
        else if (index == 5)
        {
            Cvalue += Cvalue / (double)1.4143;
        }
        else if (index == 6)
        {
            Cvalue += Cvalue / (double)1.4144;
        }
        else if (index == 7)
        {
            Cvalue += Cvalue / (double)1.4145;
        }
        else if (index == 8)
        {
            Cvalue += Cvalue / (double)1.4146;
        }
        else if (index == 9)
        {
            Cvalue += Cvalue / (double)1.4147;
        }
        else if (index == 10)
        {
            Cvalue += Cvalue / (double)1.4148;
        }
        else if (index == 11)
        {
            Cvalue += Cvalue / (double)1.4149;
        }
        else if (index == 12)
        {
            Cvalue += Cvalue / (double)1.41401;
        }
        else if (index == 13)
        {
            Cvalue += Cvalue / (double)1.4121;
        }
        else if (index == 14)
        {
            Cvalue += Cvalue / (double)1.4124;
        }
        else if (index == 15)
        {
            Cvalue += Cvalue / (double)1.41214;
        }
        else if (index == 16)
        {
            Cvalue += Cvalue / (double)3.14159246;
        }
        else if (index == 17)
        {
            Cvalue += Cvalue / (double)2.7182843;
        }
        else if (index == 18)
        {
            Cvalue += Cvalue / (double)1.414145;
        }
        else if (index == 19)
        {
            Cvalue += Cvalue / (double)1.414122;
        }
        else if (index == 20)
        {
            Cvalue += Cvalue / (double)1.41423;
        }
        else if (index == 21)
        {
            Cvalue += Cvalue / (double)1.41444;
        }
        else if (index == 22)
        {
            Cvalue += Cvalue / (double)1.41453;
        }
        else if (index == 23)
        {
            Cvalue += Cvalue / (double)1.43146;
        }
        else if (index == 24)
        {
            Cvalue += Cvalue / (double)1.24147;
        }
        else if (index == 25)
        {
            Cvalue += Cvalue / (double)1.14148;
        }
        else if (index == 26)
        {
            Cvalue += Cvalue / (double)1.41149;
        }
        else if (index == 27)
        {
            Cvalue += Cvalue / (double)1.414201;
        }
        else if (index == 28)
        {
            Cvalue += Cvalue / (double)(1.41218 + 28);
        }
        else if (index == 29)
        {
            Cvalue += Cvalue / (double)(1.41214 + 29);
        }
        else if (index == 30)
        {
            Cvalue += Cvalue / (double)(1.41214 + 30);
        }
        else if (index == 31)
        {
            Cvalue += Cvalue / (double)(1.41214 + 31);
        }*/
    }
    setElement(C, row, col, Cvalue);
}



void GPU_Test()
{
	int width = w;
    int height = w;
    Matrix *A, *B, *C;
    cudaMallocManaged((void**)&A, sizeof(Matrix));
    cudaMallocManaged((void**)&B, sizeof(Matrix));
    cudaMallocManaged((void**)&C, sizeof(Matrix));

    int nBytes = width * height * sizeof(float);

    cudaMallocManaged((void**)&A->elements, nBytes);
    cudaMallocManaged((void**)&B->elements, nBytes);
    cudaMallocManaged((void**)&C->elements, nBytes);

    A->height = height;
    A->width = width;
    B->height = height;
    B->width = width;
    C->height = height;
    C->width = width;

    for (int i = 0; i < width * height; ++i)
    {
        A->elements[i] = rand();// + 1.0;
        //printf("%d \n",((int)A->elements[i] % 23));
		B->elements[i] = rand();// + 2.0;
    }

    dim3 blockSize(32, 32);
    dim3 gridSize((width + blockSize.x - 1) / blockSize.x, (height + blockSize.y - 1) / blockSize.y);

    struct timeval t1,t2;
    gettimeofday(&t1,NULL);
    double timeuse;

    matMulKernel<<<gridSize, blockSize>>>(A, B, C);

    cudaDeviceSynchronize();

    gettimeofday(&t2,NULL);
    timeuse = t2.tv_sec - t1.tv_sec + (t2.tv_usec - t1.tv_usec)/1000000.0;
    printf("GPU Use Time:%fs\n", timeuse);

}

int main()
{
	//CPU_Test();
	GPU_Test();
	return 0;
}
