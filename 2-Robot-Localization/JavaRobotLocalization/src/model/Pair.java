package model;

public class Pair {
	
	private Position p;
	private double d;
	
	public Pair(Position p, double d) {
		this.p = p;
		this.d = d;
	}
	
	public Position getPosition() {
		return p;
	}
	
	public double getProbability() {
		return d;
	}
	
	public void setPosition(Position p) {
		this.p = p;
	}
	
	public void setProbability(double d) {
		this.d = d;
	}
}