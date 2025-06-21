package btree

import (
	"cmp"
	"math"
	"reflect"
)

type Page[K cmp.Ordered] struct {
	capacity int
	size     int
	nodes    []Node[K]
	isLeaf   bool
}

type Node[K cmp.Ordered] struct {
	key   K
	value []byte
	left  *Page[K]
	right *Page[K]
}

func New[K cmp.Ordered](size int) Page[K] {
	capacity := int(math.Floor(float64(size) / float64(reflect.TypeOf(([]Node[K])(nil)).Size())))
	nodes := make([]Node[K], capacity)
	return Page[K]{
		capacity: capacity,
		size:     0,
		nodes:    nodes,
	}
}

func newPage[K cmp.Ordered](capacity int, isLeaf bool) Page[K] {
	nodes := make([]Node[K], capacity)
	return Page[K]{
		capacity: capacity,
		size:     0,
		nodes:    nodes,
		isLeaf:   isLeaf,
	}
}

func (p *Page[K]) Find(key K) []byte {
	if p.size == 0 {
		return nil
	}
	currentPage := p
	for {
		index := currentPage.findIndexOfKey(key)
		if currentPage.nodes[index].key == key {
			return currentPage.nodes[index].value
		} else if currentPage.nodes[index].key > key {
			currentPage = currentPage.nodes[index].left
		} else {
			currentPage = currentPage.nodes[index].right
		}
		if currentPage == nil {
			break
		}
	}
	return nil
}

func (p *Page[K]) Insert(key K, value []byte) *Page[K] {
	var parentPage *Page[K] = nil
	currentPage := p
	currentParent := p
	currentPageIsOnLeft := true
	currentPageIndex := 0

	if currentPage.isFull() {
		newPage := newPage[K](currentPage.capacity, false)
		parentPage = &newPage
		upwardsNode := currentPage.split()
		parentPage.acceptNode(upwardsNode, true, 0)
		currentParent = parentPage
		currentPage = parentPage
	}

	for !currentPage.isLeaf {
		if currentPage.isFull() {
			upwardsNode := currentPage.split()
			parentPage.acceptNode(upwardsNode, currentPageIsOnLeft, currentPageIndex)
		}
		index := currentPage.findIndexOfKey(key)
		if currentPage.nodes[index].key == key {
			currentPage.nodes[index].value = value
			return currentParent
		} else if currentPage.nodes[index].key > key {
			parentPage = currentPage
			currentPage = currentPage.nodes[index].left
		} else {
			parentPage = currentPage
			currentPage = currentPage.nodes[index].right
		}
	}

	index := currentPage.findIndexOfKey(key)
	currentPage.makeSpaceAtIndex(index)
	currentPage.nodes[index] = Node[K]{key, value, nil, nil}
	return currentParent
}

func (p *Page[K]) Delete(key K) {
}

func (p *Page[K]) findIndexOfKey(key K) int {
	middle := int(math.Floor(float64(p.size) / 2.0))
	start := 0
	end := p.size
	for middle >= 0 && middle < p.size {
		if p.nodes[middle].key == key {
			return middle
		} else if p.nodes[middle].key > key {
			leftSize := len(p.nodes[start:middle])
			middle = middle - (int(math.Floor(float64(leftSize)/2.0)) + 1)
			end = middle
		} else {
			rightSize := len(p.nodes[(middle + 1):end])
			middle = middle + (int(math.Floor(float64(rightSize)/2.0)) + 1)
			start = middle
		}
	}
	return start
}

func (p *Page[K]) split() Node[K] {
	middle := int(math.Floor(float64(p.size) / 2.0))
	newPage := newPage[K](p.capacity, p.isLeaf)
	copy(newPage.nodes, p.nodes[(middle+1):p.size])
	/*
		for i := middle; i < p.size; i++ {
			p.nodes[i] = BTreeNode[K]{}
		}
	*/
	p.size = middle
	newPage.size = p.size - middle - 1
	removedNode := p.nodes[middle]
	removedNode.left = p
	removedNode.right = &newPage
	return removedNode
}

func (p *Page[K]) acceptNode(node Node[K], toLeft bool, ofIndex int) {
	var nodeLocation int
	if toLeft {
		nodeLocation = ofIndex
	} else {
		nodeLocation = ofIndex + 1
	}
	p.makeSpaceAtIndex(nodeLocation)
	p.nodes[nodeLocation] = node
	if nodeLocation < p.size {
		p.nodes[nodeLocation+1].left = p.nodes[nodeLocation].right
	}
	if nodeLocation > 0 {
		p.nodes[nodeLocation-1].right = p.nodes[nodeLocation].left
	}
	p.size += 1
}

func (p *Page[K]) makeSpaceAtIndex(index int) {
	for i := p.size; i > index; i-- {
		p.nodes[i] = p.nodes[i-1]
	}
}

func (p *Page[K]) isFull() bool {
	return p.size == p.capacity
}
