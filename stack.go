package main

import (
	"sync"
)

type Item string

type ItemStack struct {
	items []Item
	lock  sync.RWMutex
}

// Constructor for Stack
func (s *ItemStack) New() *ItemStack {
	s.items = []Item{}
	return s
}

// Adds Item to the top of the stack
func (s *ItemStack) Push(t Item) {
	s.lock.Lock()
	s.items = append(s.items, t)
	s.lock.Unlock()
}

// Removes Item from the top of the stack
func (s *ItemStack) Pop() *Item {
	s.lock.Lock()
	item := s.items[len(s.items)-1]
	s.items = s.items[0 : len(s.items)-1]
	s.lock.Unlock()
	return &item
}
