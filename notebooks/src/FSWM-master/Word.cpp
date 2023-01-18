#include "Word.h"

Word::Word(int32_t pos, uint32_t key)
{
	this->pos=pos;
	this->key=key;
}

uint32_t Word::getKey()
{
	return key;
}

int32_t Word::getPos()
{
	return pos;
}

int32_t* Word::getPosPointer()
{
	return &pos;
}

void Word::setKey(uint32_t key)
{
	this->key=key;
}

