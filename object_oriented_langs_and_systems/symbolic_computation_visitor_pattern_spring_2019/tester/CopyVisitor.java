package hw1;

import grt.*;
import grt.MathExpression;
import grt.MathVisitor;
import grt.Num;
import grt.Op;
import grt.Sym;
import grt.Var;

public class CopyVisitor implements MathVisitor<grt.MathExpression> {

    @Override
    public grt.MathExpression visit(grt.Num num) {
        return new Num(num.getValue());
    }

    @Override
    public grt.MathExpression visit(grt.Op op) {
        return new Op(new String(op.getOperand()),op.getFirst().accept(this),op.getSecond().accept(this));
    }

    @Override
    public grt.MathExpression visit(grt.Sym sym) {
        return new Sym(new String(sym.getValue()));
    }

    @Override
    public MathExpression visit(grt.Var var) {
        grt.Var cpy = new Var(var.getId());
        if(var.getPreviousMatch() != null)
            cpy.setPreviousMatch(var.getPreviousMatch().accept(this));
        return cpy;
    }
}
