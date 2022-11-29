package hw1;

import grt.Document;
import grt.EquationText;
import grt.Paragraph;
import grt.TextVisitor;

import java.util.ArrayList;
import java.util.stream.Collectors;

public class ConvertToHw1DocVisitor implements TextVisitor<hw1.DocElement> {

    ConvertToHw1Visitor convertToHw1Visitor = new ConvertToHw1Visitor();

    @Override
    public hw1.DocElement visit(Document document) {
        hw1.Document hw1doc = new hw1.Document(document.getTitle());
        ArrayList<hw1.DocElement> hw1docInner = new ArrayList(
                document.getElements().stream().map( x -> x.accept(this)).collect(
                Collectors.toList()
        ));
        hw1doc.setElements(hw1docInner);
        return hw1doc;
    }

    @Override
    public hw1.DocElement visit(Paragraph paragraph) {
        return new hw1.Paragraph(new String(paragraph.getText()));
    }

    @Override
    public hw1.DocElement visit(EquationText eq) {
        return new hw1.EquationText(eq.getInnerMath().accept(convertToHw1Visitor));
    }
}
