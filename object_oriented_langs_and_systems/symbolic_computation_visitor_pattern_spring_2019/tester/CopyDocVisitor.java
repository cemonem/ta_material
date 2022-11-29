package hw1;

import grt.DocElement;
import grt.Document;
import grt.EquationText;
import grt.Paragraph;
import grt.TextVisitor;

import java.util.ArrayList;
import java.util.stream.Collectors;

public class CopyDocVisitor implements TextVisitor<grt.DocElement> {

    CopyVisitor copyVisitor = new CopyVisitor();
    @Override
    public grt.DocElement visit(grt.Document document) {
        grt.Document copy = new Document(document.getTitle());
        ArrayList<grt.DocElement> innerDoc = new ArrayList<>(document.getElements().stream().map(
                x -> x.accept(this)
        ).collect(Collectors.toList()));
        copy.setElements(innerDoc);
        return copy;
    }

    @Override
    public grt.DocElement visit(grt.Paragraph paragraph) {
        return new Paragraph(paragraph.getText());
    }

    @Override
    public DocElement visit(grt.EquationText eq) {
        return new EquationText(eq.getInnerMath().accept(copyVisitor));
    }
}
