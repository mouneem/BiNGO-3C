#include "Bucket.h"

/*Bucket::Bucket(std::vector<Word>::iterator startS1, std::vector<Word>::iterator endS1, std::vector<Word>::iterator startS2, std::vector<Word>::iterator endS2)
{
	largeBucketStartS1 	= startS1;
	largeBucketEndS1 	= endS1;
	largeBucketStartS2	= startS2;
	largeBucketEndS2	= endS2;

	this->startS1 = startS1;
	this->startS2 = startS2;
	this->endS1   = startS1;
	this->endS2   = startS2;
}*/

Bucket::Bucket(	std::vector<Word>::iterator startS1, std::vector<Word>::iterator endS1, std::vector<Word>::iterator startS2, std::vector<Word>::iterator endS2,
				std::vector<Word>::iterator startS2Rev, std::vector<Word>::iterator endS2Rev)
{
	largeBucketStartS1 	= startS1;
	largeBucketEndS1 	= endS1;
	largeBucketStartS2	= startS2;
	largeBucketEndS2	= endS2;

	this->startS1 = startS1;
	this->startS2 = startS2;
	this->endS1   = startS1;
	this->endS2   = startS2;

	largeBucketStartS2Rev	= startS2Rev;
	largeBucketEndS2Rev		= endS2Rev;

	this->startS2Rev = startS2Rev;
	this->endS2Rev   = startS2Rev;
}

bool Bucket::hasNext()
{
	startS1 = endS1;
	startS2 = endS2;
	startS2Rev = endS2Rev;


	while(startS1 != largeBucketEndS1 && (startS2 != largeBucketEndS2 || startS2Rev != largeBucketEndS2Rev))
	{
		while(startS2 != largeBucketEndS2 && startS1->getKey() > startS2->getKey() )
			startS2++;
		
		while(startS2Rev != largeBucketEndS2Rev && startS1->getKey() > startS2Rev->getKey() )
			startS2Rev++;

		if( (startS2 != largeBucketEndS2 && startS1->getKey() == startS2->getKey()) || (startS2Rev != largeBucketEndS2Rev && startS1->getKey() == startS2Rev->getKey()))
		{
			endS2 = startS2;
			endS2Rev = startS2Rev;
			if(startS2 != largeBucketEndS2  && startS1->getKey() == startS2->getKey())
			{
				while(++endS2 != largeBucketEndS2 && (endS2 - 1 )->getKey() == endS2->getKey()  );
			}
			if(startS2Rev != largeBucketEndS2Rev && startS1->getKey() == startS2Rev->getKey())
			{
				while(++endS2Rev != largeBucketEndS2Rev && (endS2Rev - 1 )->getKey() == endS2Rev->getKey()  );
			}
			endS1 = startS1;
			while(++endS1 != largeBucketEndS1 && (endS1 - 1 )->getKey() == endS1->getKey()  );
			return 1;
		}
		startS1++;
	}
	return 0;
}

/*bool Bucket::hasNext()
{
	startS1 = endS1;
	startS2 = endS2;
	while(startS1 != largeBucketEndS1 && startS2 != largeBucketEndS2)
	{
		if(startS1->getKey() > startS2->getKey())
			startS2++;
		else if(startS1->getKey() < startS2->getKey())
			startS1++;
		else
		{
			endS1 = startS1;
			endS2 = startS2;
			while(++endS1 != largeBucketEndS1 && (endS1 - 1 )->getKey() == endS1->getKey()  );
			while(++endS2 != largeBucketEndS2 && (endS2 - 1 )->getKey() == endS2->getKey()  );
			return 1;
		}
	}
	return 0;
}*/

std::vector<Word>::iterator Bucket::getStartS1()
{
	return startS1;
}

std::vector<Word>::iterator Bucket::getStartS2()
{
	return startS2;
}

std::vector<Word>::iterator Bucket::getStartS2Rev()
{
	return startS2Rev;
}

std::vector<Word>::iterator Bucket::getEndS1()
{
	return endS1;
}

std::vector<Word>::iterator Bucket::getEndS2()
{
	return endS2;
}

std::vector<Word>::iterator Bucket::getEndS2Rev()
{
	return endS2Rev;
}