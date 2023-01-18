#ifndef BUCKET_H_
#define BUCKET_H_

#include "Word.h"
#include "Seed.h"
#include "Sequence.h"

class Bucket{

	private:
		std::vector<Word>::iterator largeBucketStartS1;
		std::vector<Word>::iterator largeBucketStartS2;
		std::vector<Word>::iterator largeBucketEndS1;
		std::vector<Word>::iterator largeBucketEndS2;

		std::vector<Word>::iterator startS1;
		std::vector<Word>::iterator startS2;
		std::vector<Word>::iterator endS1;
		std::vector<Word>::iterator endS2;

		std::vector<Word>::iterator largeBucketStartS2Rev;
		std::vector<Word>::iterator largeBucketEndS2Rev;

		std::vector<Word>::iterator startS2Rev;
		std::vector<Word>::iterator endS2Rev;

	public:
		//Bucket(std::vector<Word>::iterator  startS1, std::vector<Word>::iterator endS1, std::vector<Word>::iterator startS2, std::vector<Word>::iterator endS2);

		Bucket(	std::vector<Word>::iterator startS1, std::vector<Word>::iterator endS1, std::vector<Word>::iterator startS2, std::vector<Word>::iterator endS2,
				std::vector<Word>::iterator startS2Rev, std::vector<Word>::iterator endS2Rev);

		std::vector<Word>::iterator getStartS1();
		std::vector<Word>::iterator getStartS2();
		std::vector<Word>::iterator getStartS2Rev();
		std::vector<Word>::iterator getEndS1();
		std::vector<Word>::iterator getEndS2();
		std::vector<Word>::iterator getEndS2Rev();

		bool hasNext();
};






#endif