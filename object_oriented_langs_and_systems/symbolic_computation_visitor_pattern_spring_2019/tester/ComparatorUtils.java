package hw1;

import hw1.*;

import java.util.Random;

public class ComparatorUtils {

    public static boolean cmpNums(Num num, grt.Num grt)
    {
        return num.getValue() == grt.getValue();
    }

    public static boolean cmpPrintMath(MathExpression exp, grt.MathExpression grt)
    {
        String str = exp.accept(new PrintMathMLVisitor()).replaceAll("\\s+","");
        String grt0 = grt.accept(new grt.PrintMathMLVisitor2(0)).replaceAll("\\s+","");
        String grt1 = grt.accept(new grt.PrintMathMLVisitor2(1)).replaceAll("\\s+","");
        return grt0.equals(str) || grt1.equals(str);
    }

    public static boolean cmpPrintHTML(DocElement text, grt.DocElement grt)
    {
        String str = text.accept(new PrintHTMLVisitor()).replaceAll("\\s+","");
        String grt0 = grt.accept(new grt.PrintHTMLVisitor2(0,0,0)).replaceAll("\\s+","");
        String grt1 = grt.accept(new grt.PrintHTMLVisitor2(0,0,1)).replaceAll("\\s+","");
        String grt2 = grt.accept(new grt.PrintHTMLVisitor2(0,1,0)).replaceAll("\\s+","");
        String grt3 = grt.accept(new grt.PrintHTMLVisitor2(0,1,1)).replaceAll("\\s+","");
        String grt4 = grt.accept(new grt.PrintHTMLVisitor2(1,0,0)).replaceAll("\\s+","");
        String grt5 = grt.accept(new grt.PrintHTMLVisitor2(1,0,1)).replaceAll("\\s+","");
        String grt6 = grt.accept(new grt.PrintHTMLVisitor2(1,1,0)).replaceAll("\\s+","");
        String grt7 = grt.accept(new grt.PrintHTMLVisitor2(1,1,1)).replaceAll("\\s+","");
        return grt0.equals(str) ||
                grt1.equals(str) ||
                grt2.equals(str) ||
                grt3.equals(str) ||
                grt4.equals(str) ||
                grt5.equals(str) ||
                grt6.equals(str) ||
                grt7.equals(str);
    }

    public static boolean cmpDocuments(Document hw1, grt.Document grt){
        for(int i = 0; i < grt.getElements().size(); i++) {
            if(!cmpDocs(hw1.getElements().get(i), grt.getElements().get(i)))
                    return false;
        }
        return true;
    }

    public static boolean cmpParagraphs(Paragraph hw1, grt.Paragraph grt){
        return grt.getText().equals(hw1.getText());
    }

    public static boolean cmpEquations(EquationText hw1, grt.EquationText grt){
        return cmpExps(hw1.getInnerMath(),grt.getInnerMath());
    }

    public static boolean cmpDocs(DocElement hw1, grt.DocElement grt){
        try {
            if (grt instanceof grt.Document)
                return cmpDocuments((Document) hw1, (grt.Document) grt);
            else if (grt instanceof grt.Paragraph)
                return cmpParagraphs((Paragraph)hw1, (grt.Paragraph)grt);
            else if (grt instanceof  grt.EquationText)
                return cmpEquations((EquationText) hw1, (grt.EquationText) grt);
        }
        catch (Exception ignored)
        {
            return false;
        }

        return false;
    }

    public static boolean cmpSyms(Sym sym,grt.Sym grt)
    {
        return sym.getValue().equals(grt.getValue());
    }

    public static boolean cmpVarIds(Var var,grt.Var grt)
    {
        return var.getId() == grt.getId();
    }

    public static boolean cmpVars(Var var,grt.Var grt)
    {
        return cmpVarIds(var,grt) && cmpExps(var.getPreviousMatch(),grt.getPreviousMatch());
    }

    public static boolean cmpOpSyms(Op op,grt.Op grt)
    {
        return op.getOperand().equals(grt.getOperand());
    }

    public static boolean cmpOps(Op op,grt.Op grt)
    {
        return cmpOpSyms(op,grt) && cmpExps(op.getFirst(),grt.getFirst())
                && cmpExps(op.getSecond(),grt.getSecond());
    }

    public static boolean cmpExps(MathExpression exp,grt.MathExpression grt)
    {
        try {
            if (exp == null && grt == null) return true;

            if (grt instanceof grt.Op) {
                return cmpOps((Op) exp, (grt.Op) grt);
            } else if (grt instanceof grt.Var) {
                return cmpVars((Var) exp, (grt.Var) grt);
            } else if (grt instanceof grt.Sym) {
                return cmpSyms((Sym) exp, (grt.Sym) grt);
            } else if (grt instanceof grt.Num) {
                return cmpNums((Num) exp, (grt.Num) grt);
            }
        }
        catch(Exception e)
        {
            return false;
        }

        return false;
    }
}
