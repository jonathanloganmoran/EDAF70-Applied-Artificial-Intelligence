package model;

import java.awt.Point;
import java.util.Random;

public class Sensor {
	
	private Grid grid;
	private double L;
	private double L_s;
	private double L_s2;
	private Random rand;
	
	/**
	 * The sensor reports the estimated robot location based on a probability of error.
	 * 
	 * The sensor reports:
	 * 		The true location of the robot L with probability 0.1.
	 *   	Any of the n_Ls existing surrounding fields L_s with probability 0.05 each.
	 *   	Any of the n_Ls2 existing "secondary" surrounding fields L_s2 with probability 0.024 each.
	 *   	None with probability 1.0 - 0.1 - n_Ls  0.05 - n_Ls2 * 0.025.
	 * 
	 * @param 	grid		The grid world environment.
	 * @param 	L			Probability of the sensor reporting the true location of the robot.
	 * @param 	L_s			Probability of the sensor reporting "one step off".
	 * @param 	L_s2		Probability of the sensor reporting "two steps off".
	 */
	public Sensor(Grid grid, double L, double L_s, double L_s2) {
		this.grid = grid;
		this.L = L;
		this.L_s = L_s;
		this.L_s2 = L_s2;
		this.rand = new Random();
	}
	
	/**
	 * Gives an approximate location estimate relative to the robot's true position.
	 * 
	 * A noisy sensor model is used with a known probability of error. Assumes that robot's
	 * true location is reported with a given probability, or that one of the randomly selected
	 * surrounding or 'secondary' surrounding locations are reported with a probability relative
	 * to the number of valid neighbouring locations (considering 'walls' and corners).
	 * 
	 * @return	Position	The estimated location of the robot according to the sensor model.	
	 */
	public Position senseLocation() {
		double prob = rand.nextDouble();
		grid.getCurrentPosition().updateNeighbours(grid.rows, grid.cols);
		int n_Ls = grid.getCurrentPosition().immediateNeighbours.size();
		int n_Ls2 = grid.getCurrentPosition().outerNeighbours.size();
		
		if (prob <= L) {
			/* Return true location of robot */
			return grid.getCurrentPosition();
		}
		else if (prob <= L + L_s * n_Ls) {
			/* Return random location one step off */
			return grid.getRandomAdjacent();
		}
		else if (prob <= L + L_s * n_Ls + L_s2 * n_Ls2) {
			/* Return random location two steps off */
			return grid.getRandomOuter();
		}
		else {
			/* Return "nothing" reading */
			return new Position(new Point(-1, -1), -1);
		}
	}
}
