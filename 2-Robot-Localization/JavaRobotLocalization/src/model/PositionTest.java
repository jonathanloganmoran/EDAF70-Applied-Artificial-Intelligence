package model;

import static org.junit.Assert.*;

import java.awt.Point;
import java.util.ArrayList;
import java.util.Iterator;

import org.junit.Test;

public class PositionTest {

	@Test
	public void testGetX() {
		Position testX = new Position(new Point(1, 1), Position.NORTH);
		assertEquals(1, testX.getX());
	}

	@Test
	public void testGetY() {
		Position testY = new Position(new Point(1, 1), Position.NORTH);
		assertEquals(1, testY.getY());
	}

	@Test
	public void testGetHeading() {
		Position testH = new Position(new Point(1, 1), Position.NORTH);
		assertEquals(Position.NORTH, testH.getHeading());
	}

	@Test
	public void testgetDirectNeighbours1() {
		int rows = 8, cols = 8;
		Position testDirectNeighbours = new Position(new Point(0, 0), Position.NORTH);
		ArrayList<Position> expectedDirectNeighbours = new ArrayList<Position>();
		// Expected neighbours
		Position down = new Position(new Point(0, 1), Position.SOUTH);
		Position right = new Position(new Point(1, 0), Position.EAST);
		expectedDirectNeighbours.add(down);
		expectedDirectNeighbours.add(right);
		// Expected size of lists to be equal
		assertEquals(expectedDirectNeighbours.size(), testDirectNeighbours.getDirectNeighbours(rows, cols).size());
	}
	
	@Test
	public void testgetDirectNeighbours2() {
		int rows = 8, cols = 8;
		Position testDirectNeighbours2 = new Position(new Point(3, 3), Position.NORTH);
		ArrayList<Position> expectedDirectNeighbours2 = new ArrayList<Position>();
		// Expected neighbours
		Position up = new Position(new Point(3, 2), Position.NORTH);
		Position down = new Position(new Point(3, 4), Position.SOUTH);
		Position right = new Position(new Point(4, 3), Position.EAST);
		Position left = new Position(new Point(2, 3), Position.WEST);
		expectedDirectNeighbours2.add(up);
		expectedDirectNeighbours2.add(down);
		expectedDirectNeighbours2.add(right);
		expectedDirectNeighbours2.add(left);
		// Expected size of lists to be equal
		assertEquals(expectedDirectNeighbours2.size(), testDirectNeighbours2.getDirectNeighbours(rows, cols).size());
	}

	@Test
	public void testUpdateNeighbours1() {
		int rows = 8, cols = 8;
		Position testUpdateNeighbours = new Position(new Point(0, 0), Position.NORTH);
		// Set to empty list
		testUpdateNeighbours.immediateNeighbours = new ArrayList<Position>();
		// Update list with actual (non-empty) neighbours
		testUpdateNeighbours.updateNeighbours(rows, cols);
		// Check if function call updated empty list
		assertFalse(testUpdateNeighbours.immediateNeighbours.isEmpty());
	}
	
	@Test
	public void testUpdateNeighbours2() {
		int rows = 8, cols = 8;
		Position testUpdateNeighbours2 = new Position(new Point(0, 0), Position.NORTH);
		// Set to empty lists
		testUpdateNeighbours2.immediateNeighbours = new ArrayList<Position>();
		testUpdateNeighbours2.outerNeighbours = new ArrayList<Position>();
		ArrayList<Position> expectedImmediateNeighbours = new ArrayList<Position>();
		ArrayList<Position> expectedOuterNeighbours = new ArrayList<Position>();
		// Expected neighbours
		Position south1 = new Position(new Point(0, 1), Position.EAST);
		Position east1 = new Position(new Point(1, 0), Position.EAST);
		Position se1 = new Position(new Point(1, 1), Position.SOUTH);
		Position east2 = new Position(new Point(2, 0), Position.EAST);
		Position south2 = new Position(new Point(0, 2), Position.EAST);
		Position sse2 = new Position(new Point(1, 2), Position.SOUTH);
		Position ese2 = new Position(new Point(2, 1), Position.SOUTH);
		Position se2 = new Position(new Point(2, 1), Position.SOUTH);
		expectedImmediateNeighbours.add(se1);
		expectedImmediateNeighbours.add(east1);
		expectedImmediateNeighbours.add(south1);
		expectedOuterNeighbours.add(east2);
		expectedOuterNeighbours.add(south2);
		expectedOuterNeighbours.add(sse2);
		expectedOuterNeighbours.add(ese2);
		expectedOuterNeighbours.add(se2);
		// Update neighbours of Position from empty to actual
		testUpdateNeighbours2.updateNeighbours(rows, cols);
		// Expected size of lists to be equal
		assertEquals(expectedImmediateNeighbours.size(), testUpdateNeighbours2.immediateNeighbours.size());
		assertEquals(expectedOuterNeighbours.size(), testUpdateNeighbours2.outerNeighbours.size());
	}
	
	@Test
	public void testUpdateNeighbours3() {
		int rows = 8, cols = 8;
		Position testUpdateNeighbours3 = new Position(new Point(3, 3), Position.NORTH);
		// Set to empty list
		ArrayList<Position> expectedImmediateNeighbours = new ArrayList<Position>();
		// Expected neighbours
		Position north1 = new Position(new Point(3, 2), Position.NORTH);
		Position south1 = new Position(new Point(3, 4), Position.SOUTH);
		Position east1 = new Position(new Point(4, 3), Position.EAST);
		Position west1 = new Position(new Point(2, 3), Position.WEST);
		Position nw1 = new Position(new Point(2, 2), Position.WEST);
		Position ne1 = new Position(new Point(4, 2), Position.EAST);
		Position se1 = new Position(new Point(4, 4), Position.SOUTH);
		Position sw1 = new Position(new Point(2, 4), Position.SOUTH);
		expectedImmediateNeighbours.add(north1);
		expectedImmediateNeighbours.add(south1);
		expectedImmediateNeighbours.add(east1);
		expectedImmediateNeighbours.add(west1);
		expectedImmediateNeighbours.add(nw1);
		expectedImmediateNeighbours.add(ne1);
		expectedImmediateNeighbours.add(se1);
		expectedImmediateNeighbours.add(sw1);
		// Update neighbours of Position from empty to actual
		testUpdateNeighbours3.updateNeighbours(rows, cols);
		// Expected size of lists to be equal
		assertEquals(expectedImmediateNeighbours.size(), testUpdateNeighbours3.immediateNeighbours.size());
	}

	@Test
	public void testUpdateNeighbours4() {
		int rows = 8, cols = 8;
		Position testUpdateNeighbours4 = new Position(new Point(3, 3), Position.NORTH);
		// Set to empty list
		testUpdateNeighbours4.outerNeighbours = new ArrayList<Position>();
		// Expected neighbours
		ArrayList<Position> expectedOuterNeighbours = new ArrayList<Position>();
		Position north2 = new Position(new Point(3, 1), Position.NORTH);
		Position nnw2 = new Position(new Point(2, 1), Position.NORTH);
		Position nw2 = new Position(new Point(1, 1), Position.NORTH);
		Position wnw2 = new Position(new Point(1, 2), Position.WEST);
		Position west2 = new Position(new Point(1, 3), Position.WEST);
		Position wsw2 = new Position(new Point(1, 4), Position.WEST);
		Position sw2 = new Position(new Point(1, 5), Position.SOUTH);
		Position ssw2 = new Position(new Point(2, 5), Position.SOUTH);
		Position south2 = new Position(new Point(3, 5), Position.SOUTH);
		Position sse2 = new Position(new Point(4, 5), Position.SOUTH);
		Position se2 = new Position(new Point(5, 5), Position.SOUTH);
		Position ese2 = new Position(new Point(5, 4), Position.EAST);
		Position east2 = new Position(new Point(5, 3), Position.EAST);
		Position ene2 = new Position(new Point(5, 2), Position.EAST);
		Position ne2 = new Position(new Point(5, 1), Position.NORTH);
		Position nne2 = new Position(new Point(4, 1), Position.NORTH);
		expectedOuterNeighbours.add(north2);
		expectedOuterNeighbours.add(nnw2);
		expectedOuterNeighbours.add(nw2);
		expectedOuterNeighbours.add(wnw2);
		expectedOuterNeighbours.add(west2);
		expectedOuterNeighbours.add(wsw2);
		expectedOuterNeighbours.add(sw2);
		expectedOuterNeighbours.add(ssw2);
		expectedOuterNeighbours.add(south2);
		expectedOuterNeighbours.add(sse2);
		expectedOuterNeighbours.add(se2);
		expectedOuterNeighbours.add(ese2);
		expectedOuterNeighbours.add(east2);
		expectedOuterNeighbours.add(ene2);
		expectedOuterNeighbours.add(ne2);
		expectedOuterNeighbours.add(nne2);
		// Update neighbours of Position from empty to actual
		testUpdateNeighbours4.updateNeighbours(rows, cols);
		// Expected size of lists to be equal
		assertEquals(expectedOuterNeighbours.size(), testUpdateNeighbours4.outerNeighbours.size());
	}
	
	@Test
	public void testFacesWall() {
		int rows = 8, cols = 8;
		// Robot in top-left corner with heading in out of bounds direction
		Position testFacesWall = new Position(new Point(0, 0), Position.NORTH);
		assertTrue(testFacesWall.facesWall(rows, cols));
	}

	@Test
	public void testGetEuclideanDistance() {
		int rows = 8, cols = 8;
		// Robot in top-left corner with heading in out of bounds direction
		Position testEuclideanDistance = new Position(new Point(1, 1), Position.NORTH);
		Position toTest = new Position(new Point(3, 3), Position.NORTH);
		assertEquals(2, (int)testEuclideanDistance.getEuclideanDistance(toTest));
	}
	
	@Test
	public void testGetEuclideanDistance2() {
		int rows = 8, cols = 8;
		Position test = new Position(new Point(3, 3), Position.NORTH);
		ArrayList<Position> expectedOuterNeighbours = new ArrayList<Position>();
		Position north2 = new Position(new Point(3, 1), Position.NORTH);
		Position nnw2 = new Position(new Point(2, 1), Position.NORTH);
		Position nw2 = new Position(new Point(1, 1), Position.NORTH);
		Position wnw2 = new Position(new Point(1, 2), Position.WEST);
		Position west2 = new Position(new Point(1, 3), Position.WEST);
		Position wsw2 = new Position(new Point(1, 4), Position.WEST);
		Position sw2 = new Position(new Point(1, 5), Position.SOUTH);
		Position ssw2 = new Position(new Point(2, 5), Position.SOUTH);
		Position south2 = new Position(new Point(3, 5), Position.SOUTH);
		Position sse2 = new Position(new Point(4, 5), Position.SOUTH);
		Position se2 = new Position(new Point(5, 5), Position.SOUTH);
		Position ese2 = new Position(new Point(5, 4), Position.EAST);
		Position east2 = new Position(new Point(5, 3), Position.EAST);
		Position ene2 = new Position(new Point(5, 2), Position.EAST);
		Position ne2 = new Position(new Point(5, 1), Position.NORTH);
		Position nne2 = new Position(new Point(4, 1), Position.NORTH);
		expectedOuterNeighbours.add(north2);
		expectedOuterNeighbours.add(nnw2);
		expectedOuterNeighbours.add(nw2);
		expectedOuterNeighbours.add(wnw2);
		expectedOuterNeighbours.add(west2);
		expectedOuterNeighbours.add(wsw2);
		expectedOuterNeighbours.add(sw2);
		expectedOuterNeighbours.add(ssw2);
		expectedOuterNeighbours.add(south2);
		expectedOuterNeighbours.add(sse2);
		expectedOuterNeighbours.add(se2);
		expectedOuterNeighbours.add(ese2);
		expectedOuterNeighbours.add(east2);
		expectedOuterNeighbours.add(ene2);
		expectedOuterNeighbours.add(ne2);
		expectedOuterNeighbours.add(nne2);
		ArrayList<Position> outerResult = new ArrayList<Position>();
		for (Position p : expectedOuterNeighbours) {
			if (p.getEuclideanDistance(test) >= 2 && p.getEuclideanDistance(test) < 3) {
				outerResult.add(p);
			}
		}
		assertEquals(16, outerResult.size());
	}
	
	@Test 
	public void testCompareTo() {
		/* Check if (x, y) coordinates are the same */
		Position test = new Position(new Point(1, 1), Position.NORTH);
		Position toCompare = new Position(new Point(1, 1), Position.NORTH);
		assertTrue(test.compareTo(toCompare));
	}

	@Test
	public void testIsReachable() {
		/* Check if start heading points to end and is one Manhattan distance away */
		Position start = new Position(new Point(0, 0), Position.SOUTH);
		Position end = new Position(new Point(0, 1), Position.SOUTH);
		assertTrue(end.isReachable(start));
	}

	@Test
	public void testIsInBounds() {
		int rows = 8, cols = 8;
		Position testNotInBounds = new Position(new Point(-1, -1), Position.SOUTH);
		assertFalse(testNotInBounds.isInBounds(rows, cols));
	}

}
