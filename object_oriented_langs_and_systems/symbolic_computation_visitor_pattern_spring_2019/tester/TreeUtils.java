package hw1;

import grt.*;
import grt.DocElement;
import grt.Document;
import grt.EquationText;
import grt.MathExpression;
import grt.Num;
import grt.Op;
import grt.Paragraph;
import grt.Sym;
import grt.Var;

import java.util.Random;

public class TreeUtils {

    public static final String[] OPERANDS = {"+","*","/","|-"};
    public static final String[] SYMS = {"x","y","abc","t","q","r","f","g","k","i"};

    public static MathExpression generateMathExpTree(Random random, int level, int max_level, boolean addVars, boolean fillVars)
    {
        if(level <= max_level && random.nextInt(10) < 9)
        {
            String opnd = OPERANDS[random.nextInt(4)];
            return new Op(new String(opnd),generateMathExpTree(random,level+1,max_level,addVars,fillVars),
                    generateMathExpTree(random,level+1,max_level,addVars,fillVars));
        }
        else
        {
            int rnd2 = random.nextInt(10);
            rnd2 = (rnd2 * level) / max_level;

            if(addVars && rnd2 > 3)
            {
                int varId = random.nextInt(10);
                grt.Var var = new Var(varId);
                if(fillVars)
                    var.setPreviousMatch(generateMathExpTree(random,1,3,false,false));
                return var;
            }
            else
            {
                return random.nextBoolean()? new grt.Sym(new String(SYMS[random.nextInt(10)])): new Num(random.nextInt(20));
            }
        }
    }

    public static DocElement generateDocElementTree(Random random, boolean fillEqs) {
        grt.Document doc = new Document(new String(SYMS[random.nextInt(10)]));
        int numElements = random.nextInt(5)+5;
        for(int i = 0; i < numElements; i++){
            int rnd = random.nextInt(10);
            if(rnd < 5) {
                doc.add(new Paragraph(new String(SYMS[random.nextInt(10)])));
            }
            else{
                if(fillEqs){
                    doc.add(new grt.EquationText(generateMathExpTree(random,0,3,true,true)));
                }
                else{
                    doc.add(new EquationText(new Sym("")));
                }
            }
        }
        return doc;
    }

}
