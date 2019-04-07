package main

import (
	"math"
)

//HuffmanFrequenceTable HuffmanFrequenceTable
type HuffmanFrequenceTable struct {
	Table map[string]*Node
}

// initialize table
func NewHuffmanTable(text string) *HuffmanFrequenceTable {

	table := make(map[string]*Node)
	for i := 0; i < len(text); i++ {
		c := (string(text[i]))
		if table[c] == nil {
			table[c] = &Node{value: c, frequency: 1}
		} else {
			table[c].frequency++
		}
	}
	return &HuffmanFrequenceTable{Table: table}

}

// get smallest node
func (hft *HuffmanFrequenceTable) GetSmallestNode() *Node {
	smallest := &Node{frequency: math.MaxInt32}
	for _, v := range hft.Table {
		if v.frequency < smallest.frequency {
			smallest = v
		}
	}
	return smallest
}

// join 2 nodes into 1
func JoinNodes(firstNode, secondNode *Node, label string) *Node {

	return &Node{
		LeftNode:  firstNode,
		RightNode: secondNode,
		frequency:    firstNode.frequency + secondNode.frequency,
		value:     label,
	}

}
