package hw1;

import grt.*;
import grt.MathVisitor;
import grt.Num;
import grt.Op;
import grt.Sym;
import grt.Var;

public class PrintBasicVisitor implements MathVisitor<String> {
    @Override
    public String visit(Num num) {
        return Integer.toString(num.getValue());
    }

    @Override
    public String visit(Op op) {
        return "("+op.getFirst().accept(this)+op.getOperand()+op.getSecond().accept(this)+")";
    }

    @Override
    public String visit(Sym sym) {
        return sym.getValue();
    }

    @Override
    public String visit(Var var) {
        if(var.getPreviousMatch() == null)
            return "V"+var.getId();
        else
            return "V"+var.getId()+"["+var.getPreviousMatch().accept(this)+"]";
    }
}
