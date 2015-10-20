package chapter13.example;

public class TestEdible {
    public static void main(String[] args) {
        Object[] objects = {new Tiger(2), new Chicken(1), new Apple()};

        for (int i = 0; i < objects.length; i++) {
            if (objects[i] instanceof Edible)
                System.out.println(((Edible) objects[i]).howToEat());
            if (objects[i] instanceof Animal) {
                System.out.println(((Animal) objects[i]).sound());
                System.out.println("Age: " + ((Animal) objects[i]).getAge());
            }
        }
    }
}


interface Edible {
    String howToEat();
}

abstract class Animal {
    private int age;

    public Animal(int age) { this.age = age; }
    public void setAge(int age) { this.age = age; }
    public int getAge() {return age; }

    public abstract String sound();
}

class Chicken extends Animal implements Edible {
    public Chicken(int age) {
        super(age);
    }

    @Override
    public String sound() {
        return "Chicken: cock-a-doodle-doo";
    }

    @Override
    public String howToEat() {
        return "Chicken: Fry it";
    }
}

class Tiger extends Animal {
    public Tiger(int age) {
        super(age);
    }

    @Override
    public String sound() {
        return "Tiger: RROOAARR";
    }
}

abstract class Fruit implements Edible {
}

class Apple extends Fruit {
    @Override
    public String howToEat() {
        return "Apple: Make apple cider";
    }
}

class Orange extends Fruit {
    @Override
    public String howToEat() {
        return "Orange: Make orange juice";
    }
}