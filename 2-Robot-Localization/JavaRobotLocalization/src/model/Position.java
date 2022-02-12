package model;

import java.awt.Point;
import java.util.ArrayList;

public class Position {
	
	public static final int NORTH = 0;
	public static final int SOUTH = 1;
	public static final int EAST = 2;
	public static final int WEST = 3;
	
	private Point p;
	private int h;
	protected ArrayList<Position> immediateNeighbours;
	protected ArrayList<Position> outerNeighbours;
	
	public Position(Point p, int h) {
		this.p = p;
		this.h = h;
		this.immediateNeighbours = new ArrayList<Position>();
		this.outerNeighbours = new ArrayList<Position>();
	}
	
	/**
	 * The following methods return the coordinates and heading (direction) 
	 * belonging to this Position.
	 * 
	 * @return 		int 		x-, y-coordinate or heading of Position
	 */
	public int getX() {
		return (int)p.getX();
	}
	public int getY() {
		return (int)p.getY();
	}
	public int getHeading() {
		return h;
	}
	
	public int getStateIndex(int rows, int cols, int head) {
		return head * (cols * getX() + getY());
	}
	
	/**
	 * Returns the direct (von Neumann) neighbours that are within the
	 * grid bounds relative to the current position.
	 * 
	 * @param 		rows		height of the grid
	 * @param 		cols		width of the grid
	 * @return		neighbours	von Neumann neighbouring positions
	 */
	public ArrayList<Position> getDirectNeighbours(int rows, int cols) {
		// assuming (x, y) coordinates
		Position up = new Position(new Point((int)p.getX(), (int)p.getY() - 1), NORTH);
		Position down = new Position(new Point((int)p.getX(), (int)p.getY() + 1), SOUTH);
		Position right = new Position(new Point((int)p.getX() + 1, (int)p.getY()), EAST);
		Position left = new Position(new Point((int)p.getX() - 1, (int)p.getY()), WEST);
		ArrayList<Position> neighbours = new ArrayList<Position>();
		/*
		//assuming (row, col) coordinates
		Position up = new Position(new Point((int)p.getX() - 1, (int)p.getY()), NORTH);
		Position down = new Position(new Point((int)p.getX() + 1, (int)p.getY()), SOUTH);
		Position right = new Position(new Point((int)p.getX(), (int)p.getY() + 1), EAST);
		Position left = new Position(new Point((int)p.getX(), (int)p.getY() - 1), WEST);
		*/
		// check if neighbouring positions are inside the grid
		//if (up.isInBounds(rows, cols) && isReachable(up)) neighbours.add(up);
		if (up.isInBounds(rows, cols)) neighbours.add(up);
		if (down.isInBounds(rows, cols)) neighbours.add(down);
		if (right.isInBounds(rows, cols)) neighbours.add(right);
		if (left.isInBounds(rows, cols)) neighbours.add(left);
		return neighbours;
	}
	
	/**
	 * Returns the eight Moore (orthogonal and diagonal) neighbours relative to the current position.
	 * 
	 * @param 		rows		height of the grid
	 * @param 		cols		width of the grid
	 * @return 
	 */
	public void updateNeighbours(int rows, int cols) {
		for (int i = getX() - 2; i <= getX() + 2; i++) {
			for (int j = getY() - 2; j <= getY() + 2; j++) {
				// Make sure that setting existing heading goes with movement model
				Position temp = new Position(new Point(i, j), getHeading());
				// Check if in bounds and not the same coordinate
				if (temp.isInBounds(rows, cols) && !compareTo(temp)) {
					double dist = getEuclideanDistance(temp);
					if (dist < 2 && dist > 0.01) {
						immediateNeighbours.add(temp);
					}
					else if (dist >= 2 && dist < 3) {
						outerNeighbours.add(temp);
					}
				}
			}
		}
	}
	
	/**
	 * Checks if current state (x, y, h) faces a wall.
	 * 
	 * @returns		boolean		whether or not the current state faces a wall
	 */
	public boolean facesWall(int rows, int cols) {
		/*
		// assuming (row, col) coordinates
		return p.getX() == 0 && p.getY() < cols && getHeading() == NORTH
			|| p.getX() == rows - 1 && p.getY() < cols && getHeading() == SOUTH
			|| p.getX() < rows && p.getY() == cols - 1 && getHeading() == EAST
			|| p.getX() < rows && p.getY() == 0 && getHeading() == WEST;
		*/
		// assuming (x, y) coordinates
		return p.getX() < cols && p.getY() == 0 && getHeading() == NORTH
			|| p.getX() < cols && p.getY() == rows - 1 && getHeading() == SOUTH
			|| p.getX() == cols - 1 && p.getY() < rows && getHeading() == EAST
			|| p.getX() == 0 && p.getY() < rows && getHeading() == WEST;
	}
	
	/**
	 * Calculates the Euclidean distance of a given position
	 * relative to the current position.
	 * 
	 */
	public double getEuclideanDistance(Position pt) {
		return Math.sqrt(Math.pow(Math.abs(getX() - pt.getX()), 2) + 
			   Math.pow(Math.abs(getY() - pt.getY()), 2));
	}
	
	/**
	 * Checks if position p is reachable by an arbitrary position pt.
	 * A position p is reachable by pt if pt is a diagonal neighbour of p.
	 * 
	 * @returns		boolean		whether or not pt is a diagonal neighbour of p
	 */
	public boolean isReachable(Position pt) {
		// assuming positions in (x, y) coordinates and pt is is prev
		return (pt.getX() == p.getX() && pt.getY() - 1 == p.getY() && pt.getHeading() == NORTH)
				|| (pt.getX() == p.getX() && pt.getY() + 1 == p.getY() && pt.getHeading() == SOUTH)
				|| (pt.getX() + 1 == p.getX() && pt.getY() == p.getY() && pt.getHeading() == EAST)
				|| (pt.getX() - 1 == p.getX() && pt.getY() == p.getY() && pt.getHeading() == WEST);
	}
	
	public boolean isReachableFrom(Position prev) {
		// assuming positions in (x, y) coordinates
		return (prev.getX() == p.getX() && prev.getY() - 1 == p.getY() && prev.getHeading() == NORTH)
			|| (prev.getX() == p.getX() && prev.getY() + 1 == p.getY() && prev.getHeading() == SOUTH)
			|| (prev.getX() + 1 == p.getX() && prev.getY() == p.getY() && prev.getHeading() == EAST)
			|| (prev.getX() - 1 == p.getX() - 1 && prev.getY() - 1 == p.getY() && prev.getHeading() == WEST);
	}
	
	public boolean willReachXY(Position pt) {
		// assuming positions in (x, y) coordinates and pt is future -->
		return (pt.getX() == p.getX() && pt.getY() == p.getY() - 1 && getHeading() == NORTH)
			|| (pt.getX() == p.getX() && pt.getY() == p.getY() + 1 && getHeading() == SOUTH)
			|| (pt.getX() == p.getX() + 1 && pt.getY() == p.getY() && getHeading() == EAST)
			|| (pt.getX() == p.getX() - 1 && pt.getY() == p.getY() && getHeading() == WEST);
	}
	
	public boolean willReach(Position pt) {
		// assuming positions in (rows, col) coordinates and pt is future -->
		return (pt.getX() == p.getX() - 1 && pt.getY() == p.getY() && getHeading() == NORTH)
			|| (pt.getX() == p.getX() + 1 && pt.getY() == p.getY() && getHeading() == SOUTH)
			|| (pt.getX() == p.getX() && pt.getY() == p.getY() + 1 && getHeading() == EAST)
			|| (pt.getX() == p.getX() && pt.getY() == p.getY() - 1 && getHeading() == WEST);
	}
	
	/**
	 * Checks if the position is on the rows x cols 2D grid.
	 * 
	 * @param 		rows		height of the grid
	 * @param 		cols		width of the grid
	 * 
	 * @return  	boolean	whether or not the point lies on the 2D grid	
	 */
	public boolean isInBounds(int rows, int cols) {
		/*
		// assuming (row, col) coordinates
		return 0 <= p.getX() && p.getX() < rows && 0 <= p.getY() & p.getY() < cols; 
		 */
		// assuming (row, col) coordinates
		return 0 <= p.getX() && p.getX() < cols && 0 <= p.getY() && p.getY() < rows; 
	}
	
	/**
	 * Checks if the current Point p is equal to an arbitrary Point obj.
	 * Is equal if the positions (x, y) are the same.
	 * 
	 * @returns		boolean		whether or not the states are the same
	 */
	public boolean compareTo(Object obj) {
		Point pt = ((Position) obj).p;
		return p.getX() == pt.getX() && p.getY() == pt.getY();
	}
	
	/**
	 * Checks if the current state p is equal to an arbitrary state obj.
	 * Is equal if the position (x, y) and heading h are the same.
	 * 
	 * @returns		boolean		whether or not the states are the same
	 */
	@Override
	public boolean equals(Object obj) {
		Position pt = (Position) obj;
		return p.getX() == pt.getX() && p.getY() == pt.getY() && getHeading() == pt.getHeading();
	}
	
	public void print() {
		double x = p.getX();
		double y = p.getY();
		if (x == -1 || y == -1) {
			// Print to console in red
			System.err.println("Position: (" + p.getX() + ", " + p.getY() +"), Heading: " + getHeading());
		}
		else {
			System.out.println("Position: (" + p.getX() + ", " + p.getY() +"),   Heading: " + getHeading());
		}
	}
}
