package model;

import java.awt.Point;
import java.util.ArrayList;
import java.util.Random;

public class Grid {
	
	public int rows, cols;
	public int head;
	private Random rand;
	private Position currentPosition;
	
	/**
	 * The discrete grid world environment without landmarks.
	 * 
	 * The robot agent acts on the environment by making moves to an orthogonally 
	 * adjacent location, i.e., a move in a direction (NORTH=0, SOUTH=1, EAST=2, WEST=3).
	 * Actions going off the edge of the grid result in a move to a randomly selected
	 * valid orthogonally adjacent location.
	 * 
	 * @param	rows		The height of the grid.
	 * @param 	cols		The width of the grid.
	 * @param 	head		The number of possible directions.
	 */
	public Grid(int rows, int cols, int head) {
		this.rows = rows;
		this.cols = cols;
		this.head = head;
		this.rand = new Random();
		this.setCurrentPosition(new Position(new Point(rand.nextInt(rows), rand.nextInt(cols)),
											rand.nextInt(head)));
	}
	
	/**
	 * Moves robot according to a probabilistic strategy.
	 * 
	 * The same heading h_t is selected for h_(t+1) with probability:
	 * 		P( h_(t+1)  =  h_t  |  not encountering a wall ) = 0.7
     *      P( h_(t+1)  =  h_t  |  encountering a wall     ) = 0.0
     * or a new heading h_(t+1) is selected with probability:
     * 		P( h_(t+1) !=  h_t  |  not encountering a wall ) = 0.3
     *      P( h_(t+1) !=  h_t  |  encountering a wall     ) = 1.0
	 */
	public void moveRobot() {
		ArrayList<Position> positions = getCurrentPosition().getDirectNeighbours(rows, cols);
		double prob = rand.nextDouble();
		if (prob <= 0.3 || getCurrentPosition().facesWall(rows, cols)) {
			positions.removeIf(p -> p.getHeading() == getCurrentPosition().getHeading());
			// Move robot one step in new direction
			Position next = positions.get(rand.nextInt(positions.size()));
			try {
				setCurrentPosition(next);
			}
			catch(IndexOutOfBoundsException e) {
				System.err.println("Out of bounds, trying another random move.");
				positions.remove(next);
				setCurrentPosition(positions.get(rand.nextInt(positions.size())));
			}
		}
		else {
			// Move robot one step in same direction
			int x = getCurrentPosition().getX();
			int y = getCurrentPosition().getY();
			int h = getCurrentPosition().getHeading();
			switch (h) {
				case 0: setCurrentPosition(new Position(new Point(x, y - 1), head)); break;
				case 1: setCurrentPosition(new Position(new Point(x, y + 1), head)); break;
				case 2: setCurrentPosition(new Position(new Point(x + 1, y), head)); break;
				case 3: setCurrentPosition(new Position(new Point(x - 1, y), head)); break;
			}
		}
	}
	
	/**
	 * Sensor reports a randomly selected valid orthogonally adjacent location.
	 * 
	 * @return	randAdjacent	One of the valid neighbouring locations.
	 */
	public Position getRandomAdjacent() {
		getCurrentPosition().updateNeighbours(rows, cols);
		int randIdx = rand.nextInt(getCurrentPosition().immediateNeighbours.size());
		Position randAdjacent = getCurrentPosition().immediateNeighbours.get(randIdx);
		return randAdjacent;
	}
	
	/**
	 * Sensor reports a randomly selected valid orthogonally adjacent location at radius=2.
	 * 
	 * @return	randOuter		One of the valid neighbouring locations.
	 */
	public Position getRandomOuter() {
		getCurrentPosition().updateNeighbours(rows, cols);
		int randIdx = rand.nextInt(getCurrentPosition().outerNeighbours.size());
		Position randOuter = getCurrentPosition().outerNeighbours.get(randIdx);
		return randOuter;
	}

	public Position getCurrentPosition() {
		return currentPosition;
	}

	public void setCurrentPosition(Position currentPosition) {
		this.currentPosition = currentPosition;
	}
	
	
}
