package model;

import java.awt.Point;
import control.EstimatorInterface;


public class HMMLocalizer implements EstimatorInterface {
	
		/* For colourising the console output (ANSI plug-in required) */
		public static final String ANSI_RESET = "\u001B[0m";
		public static final String ANSI_GREEN = "\u001B[32m";
		public static final String ANSI_RED = "\u001B[31m";
		public int rows, cols;
		public int head;
		private Grid grid;
		private Sensor sensor;
		private Position[] states;
		/* Transition matrix */
		private double[][] T;
		/* Sensor matrix */
		private double[][] O;
		/* Forward vector */
		private double[] f;
		/* Debugging */
		private int nUpdates;
		private double avgDistance;
	
	/**
	 * Performs robot localisation using a Hidden Markov Model and forward update step.
	 * 
	 * This task corresponds to Exercise 15.9 in AIMA: filtering in an environment with
	 * no landmarks. Assumes a rows x cols rectangular grid with a noisy sensor that gives
	 * an approximation to the robot's location. The robot's movement model is defined in
	 * @see		Grid#moveRobot()
	 * 
	 * @param 	rows		The height of the grid.
	 * @param 	cols		The width of the grid.
	 * @param 	head		The number of possible directions.
	 */
	public HMMLocalizer(int rows, int cols, int head) {
		this.rows = rows;
		this.cols = cols;
		this.head = head;
		this.grid = new Grid(rows, cols, head);
		this.sensor = new Sensor(grid, 0.1, 0.05, 0.025);
		initForwardFiltering();
		this.T = initTransitionMatrix();
		nUpdates = 0;
		avgDistance = 0;
		
	}
	
	/** 
	 * Triggers a single move of the robot, then obtains the sensor reading and updates
	 * the observation matrix based on the reading using a forward filtering algorithm.
	 * The estimated location of the robot is calculated based on the updated probability 
	 * distribution. The distance away from the robot's actual location (in Manhattan steps) 
	 * is printed in the console along with the average error distance.
	 * 
	 * {@inheritDoc}
	 */
	@Override
	public void update() {
		grid.moveRobot();
		Position sensedLocation = sensor.senseLocation();
		f = forwardFiltering(sensedLocation);
		Pair estimate = updateEstimate();
		nUpdates++;
		sensedLocation.print();
		estimate.getPosition().print();
		printDistance(grid.getCurrentPosition(), estimate.getPosition());
	}
	
	/** 
	 * Prints the Manhattan distance between the current estimate and the actual location 
	 * of the robot `p`. Also prints the average distance, rounded to two decimals.
	 * 
	 * @param 	p			The current true location of the robot. 
	 * @param 	other		The estimated location of the robot.
	 */
	public void printDistance(Position p, Position other) {
		double dist = Math.abs(p.getX() - other.getX()) + Math.abs(p.getY() - other.getY());
		avgDistance +=  dist;
		double scale = Math.pow(10, 2);
		double scaledAvg = Math.round((avgDistance / nUpdates) * scale) / scale;
		if (dist == 0.0) {
			System.out.println(ANSI_GREEN + "Distance away: " + dist + "      Average distance: " + scaledAvg + ANSI_RESET);
		}
		else {
			System.out.println("Distance away: " + dist + "      Average distance: " + scaledAvg);
		}
	}
	
	/**
	 * Initialises the state matrices as column vectors with a uniform distribution over all 
	 * possible states i.e., the prior probabilities.
	 */
	public void initForwardFiltering() {
		int size = rows * cols * head;
		states = new Position[size];
		f = new double[size];
		int count = 0;
		for (int i = 0; i < rows; i++) {
			for (int j = 0; j < cols; j++) {
				for (int h = 0; h < head; h++) {
					Position state = new Position(new Point(i, j), h);
					states[count] = state;
					f[count] = 1.0 / size;
					count++;
				}
			}
		}
	}
	
	/** 
	 * Initialises the transition matrix according to the robot movement model.
	 *  
	 * @return	temp	The SxS transition matrix initialised with given probabilities.
	 */
	public double[][] initTransitionMatrix() {
		int size = rows * cols * head;
		double[][] temp = new double[size][size];
		for (int i = 0; i < size; i++) {
			Position current = states[i];
			for (int j = 0; j < size; j++) {
				Position other = states[j];
				if (current.willReachXY(other)) {
					current.updateNeighbours(rows, cols);
					int len = current.getDirectNeighbours(rows, cols).size();
					if (current.facesWall(rows, cols)) {
						temp[i][j] = 1.0 / len;
					}
					else if (current.getHeading() == other.getHeading()) {
						temp[i][j] = 0.7;
					}
					else {
						temp[i][j] = 0.3 / (len - 1);
					}
				}
				else {
					temp[i][j] = 0.0;
				}
			}
		}
		return temp;
	}

	
	/**
	 * Initialises the observation matrix with the likelihood of the sensor
	 * reporting 'nothing'.
	 * 
	 * @return	temp		The initialised observation matrix.
	 */
	public double[][] initObservationMatrix() {
		double[][] temp = new double[rows][cols];
		for (int i = 0; i < rows; i++) {
			for (int j = 0; j < cols; j++) {
				Position state = new Position(new Point(i, j), -1);
				state.updateNeighbours(rows, cols);
				int n_Ls = state.immediateNeighbours.size();
				int n_Ls2 = state.outerNeighbours.size();
				temp[i][j] = 1.0 - (0.1 + 0.05 * n_Ls + 0.025 * n_Ls2);
			}
		}
		return temp;
	}
	
	/**
	 * Updates the state-observation matrix given a new sensor reading.
	 * 
	 * The observation (emission) matrix of dimension SxS is a diagonal matrix whose 
	 * ith element along the diagonal is the likelihood of a state X_i having caused 
	 * the sensor reading to be detected.
	 * 
	 * @param 	reading		The observation variable i.e., the current sensor reading.
	 * @return	temp		The updated observation matrix given the sensor error model.
	 */
	public double[][] updateObservationMatrix(Position reading) {
		double[][] temp = new double[rows][cols];
		reading.updateNeighbours(rows, cols);
		for (int i = 0; i < rows; i++) {
			for (int j = 0; j < cols; j++) {
				if (reading.getX() == i && reading.getY() == j) {
					temp[i][j] = 0.1;
				}
				else {
					temp[i][j] = 0.0;
				}
				for (Position p : reading.immediateNeighbours) {
					if (p.getX() == i && p.getY() == j) {
						temp[i][j] = 0.05;
					}
				}
				for (Position p : reading.outerNeighbours) {
					if (p.getX() == i && p.getY() == j) {
						temp[i][j] = 0.025;
					}
				}
			}
		}
		return temp;
	}
	
	/**
	 * Updates the belief state after receiving a new observation (the sensor reading).
	 * 
	 * The forward matrix-vector equation 15.12 from AIMA Sect. 15.3.1 performs
	 * belief state estimation with a normalising factor alpha.
	 * 
	 * @param 	reading		The observation variable i.e., the current sensor reading.
	 * @return	f			The forward vector 
	 */
	public double[] forwardFiltering(Position reading) {
		if (reading.getX() == -1 || reading.getY() == -1) {
			reading.updateNeighbours(rows, cols);
			O = initObservationMatrix();
		}
		else {
			O = updateObservationMatrix(reading);
		}
		int size = rows * cols * head;
		double[] Ot = new double[size];
		int count = 0;
		for (int i = 0; i < cols; i++) {
			for (int j = 0; j < rows; j++) {
				for (int h = 0; h < head; h++) {
					Ot[count++] = O[i][j];
				}
			}
		}
		double sum = 0;
		double[] temp = new double[size];
		for (int i = 0; i < Ot.length; i++) {
			temp[i] = 0.0;
			for (int j = 0; j < Ot.length; j++) {
				temp[i] += Ot[i] * T[j][i] * f[j];
			}
			sum += temp[i];
		}
		for (int i = 0; i < temp.length; i++) {
			/* Normalising the column vector probabilities */
			f[i] = temp[i] / sum;
		}
		return f;
	}
	
	/**
	 * Updates the estimated location of the robot based on the probabilities stored in
	 * the column vector f.
	 * 
	 * @return	Pair	The most-likely location of the robot and its likelihood value.
	 */
	public Pair updateEstimate() {
		Point idx = new Point();
		double fMax = Double.MIN_VALUE, currentProb;
		for (int i = 0; i < rows; i++) {
			for (int j = 0; j < cols; j++) {
				currentProb = getCurrentProb(i, j);
				if (currentProb > fMax) {
					fMax = currentProb;
					idx.setLocation(i, j);
				}
			}
		}
		Pair estimate = new Pair(new Position(idx, -1), fMax);
		return estimate;
	}
	
	/**
	 * Maps position coordinates to state indices for the column vector.
	 * 
	 * @param 	x		The x-coordinate of the position.
	 * @param 	y		The y-coordinate of the position.
	 * @return	int		The index of the position in the column vector.
	 */
	public int getStateIndex(int x, int y) {
		return head * (x * cols + y);
	}
	
	/**
	 * {@inheritDoc}
	 */
	@Override
	public int getNumRows() {
		return rows;
	}
	@Override
	public int getNumCols() {
		return cols;
	}
	@Override
	public int getNumHead() {
		return head;
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public int[] getCurrentTrueState() {
		int[] ret = new int[3];
		ret[0] = grid.getCurrentPosition().getX();
		ret[1] = grid.getCurrentPosition().getY();
		ret[2] = grid.getCurrentPosition().getHeading();
		return ret;
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public int[] getCurrentReading() {
		int[] ret = new int[2];
		Position read = sensor.senseLocation();
		if (read.getX() == -1 || read.getY() == -1) {
			System.err.println("Current reading is null");
			return null;
		}
		else {
			ret[0] = read.getX();
			ret[1] = read.getY();
			return ret;
		}
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public double getCurrentProb( int x, int y) {
		double ret = 0.0;
		int idx = getStateIndex(x, y);
		for(int i = 0; i < 4; i++) {
			ret += f[idx + i];
		}
		return ret;
	}
	
	/**
	 * {@inheritDoc}
	 */
	@Override
	public double getOrXY( int rX, int rY, int x, int y, int h) {
		Position observation = new Position(new Point(x, y), h);
		O = updateObservationMatrix(observation);
		if (rX == -1 || rY == -1) {
			observation.updateNeighbours(rows, cols);
			return 1 - 0.1 - 0.05 * observation.immediateNeighbours.size() - 0.025 * observation.outerNeighbours.size();
		}
		else {
			return O[rX][rY];
		}
	}
	
	/**
	 * {@inheritDoc}
	 */
	@Override
	public double getTProb( int x, int y, int h, int nX, int nY, int nH) {
		return T[x * cols + y * cols * head + h][nX * cols + nY * cols * head + nH];
	}
	
}
