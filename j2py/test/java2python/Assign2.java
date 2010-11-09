class Assign2 {
    public static void main(String[] args) {
        int x = 42, y=7;
        System.out.println(x);

        x >>>= 1;        
        System.out.println(x);
        
        x = 2 + x >>> 1;
        System.out.println(x);
        System.out.println(y);

        y = x++;
        System.out.println("postinc'd" + x);
        System.out.println("postinc'd y " +y);
                
        y = ++x;
        System.out.println("preinc'd" + x);
        System.out.println("y " +y);
                

        y = x--;
        System.out.println("postdec'd" + x);
        System.out.println("y " +y);
                
        y = --x;
        System.out.println("predec'd" + x);
        System.out.println("y " +y);

        x++; --y;
        System.out.println(x);
        System.out.println("y " +y);
                
        --y; ++x;
        System.out.println(x);
        System.out.println("y " +y);
        
        x = 10;
        y = 2*(x++);
        
        System.out.println(x);
        System.out.println(y);


    }
}
