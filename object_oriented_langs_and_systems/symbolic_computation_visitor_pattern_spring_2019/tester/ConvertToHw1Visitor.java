package hw1;

import grt.*;
import grt.MathVisitor;
import hw1.MathExpression;

public class ConvertToHw1Visitor implements MathVisitor<MathExpression> {
    @Override
    public MathExpression visit(grt.Num num) {
        return new hw1.Num(num.getValue());
    }

    @Override
    public MathExpression visit(grt.Op op) {
        return new hw1.Op(new String(op.getOperand()),op.getFirst().accept(this),op.getSecond().accept(this));
    }

    @Override
    public MathExpression visit(grt.Sym sym) {
        return new hw1.Sym(new String(sym.getValue()));
    }

    @Override
    public MathExpression visit(grt.Var var) {
        hw1.Var hw1 = new hw1.Var(var.getId());
        if(var.getPreviousMatch() != null)
            hw1.setPreviousMatch(var.getPreviousMatch().accept(this));
        return hw1;
    }
}
