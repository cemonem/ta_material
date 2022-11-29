package hw1;

import com.google.common.collect.Lists;
import grt.*;
import grt.ClearVarsVisitor;
import grt.CountAtomicsVisitor;
import grt.Num;
import grt.Op;
import grt.Sym;
import grt.Var;

import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.Random;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;

import static hw1.TreeUtils.generateDocElementTree;
import static hw1.TreeUtils.generateMathExpTree;

public class ExampleUtils {

    public static int random_seed = 1837837;
    public static Random random = new Random(random_seed);
    public static CopyVisitor copyVisitor = new CopyVisitor();
    public static ConvertToHw1Visitor convertToHw1Visitor = new ConvertToHw1Visitor();
    public static ReplaceVarsVisitor replaceVarsVisitor = new ReplaceVarsVisitor();
    public static grt.ClearVarsVisitor clearVarsVisitor = new ClearVarsVisitor();
    public static grt.CountAtomicsVisitor countAtomicsVisitor = new CountAtomicsVisitor();
    public static CountAtomicsVisitor2 countAtomicsVisitor2 = new CountAtomicsVisitor2();
    public static CopyDocVisitor copyDocVisitor = new CopyDocVisitor();
    public static ConvertToHw1DocVisitor convertToHw1DocVisitor = new ConvertToHw1DocVisitor();

    public static List<grt.MathExpression> basicExamplesWithoutVars = List.of(
            new grt.Num(0),
            new grt.Num(2),
            new grt.Num(32),
            new grt.Sym("a"),
            new grt.Sym("xyz"),
            new grt.Op("+", new grt.Num(4), new grt.Sym("v")),
            new grt.Op("/", new grt.Num(5), new grt.Sym("h")),
            new grt.Op("*", new grt.Num(68), new Sym("l"))
    );

    public static List<grt.MathExpression> basicEmptyVars = IntStream.range(0,basicExamplesWithoutVars.size()).mapToObj(
            x -> new grt.Var(x)
    ).collect(Collectors.toList());

    private static List<grt.MathExpression> basicFilledVars() {
        grt.Var[] vars = new grt.Var[basicExamplesWithoutVars.size()];
        for (int i = 0; i < basicExamplesWithoutVars.size(); i++)
            vars[i] = new Var(i);
        for (int i = 0; i < basicExamplesWithoutVars.size(); i++)
            vars[i].setPreviousMatch(basicExamplesWithoutVars.get(i).accept(copyVisitor));
        return Arrays.stream(vars).map(x -> (grt.MathExpression) x).collect(Collectors.toList());
    }
    public static List<grt.MathExpression> basicFilledVars = basicFilledVars();

    public static List<grt.MathExpression> complexExamplesWithVars = Stream.generate(
            () -> generateMathExpTree(random, 0, 6, true, true)).limit(50).collect(Collectors.toList());

    public static List<grt.MathExpression> complexExamplesWithoutVars = complexExamplesWithVars.stream().map(
            x -> x.accept(copyVisitor).accept(replaceVarsVisitor)).collect(Collectors.toList());

    public static List<grt.MathExpression> complexExamplesWithEmptyVars = complexExamplesWithVars.stream().map(x ->
    {
        grt.MathExpression emptied = x.accept(copyVisitor);
        emptied.accept(clearVarsVisitor);
        return emptied;
    }).collect(Collectors.toList());

    public static List<grt.DocElement> basicDocuments = Stream.generate(() -> generateDocElementTree(random,
            false)).limit(10).collect(Collectors.toList());
    public static List<grt.DocElement> complexDocuments = Stream.generate(() -> generateDocElementTree(random,
            true)).limit(20).collect(Collectors.toList());


    public interface Evaluator {
        boolean apply(List<grt.MathExpression> grt, List<hw1.MathExpression> hw1);
    }

    public interface DocEvaluator {
        boolean apply(List<grt.DocElement> grt, List<hw1.DocElement> hw1);
    }

    public static double evaluateWithExamples(int except, Evaluator evaluator, List<grt.MathExpression>... examples) {
        List<List<grt.MathExpression>> cartProd = Lists.cartesianProduct(examples);
        return (double)cartProd.stream().mapToInt(x -> {
            try {
                return evaluator.apply(x.stream().map(
                        y -> y.accept(copyVisitor)).collect(Collectors.toList()),
                        x.stream().map(y -> y.accept(convertToHw1Visitor)).collect(Collectors.toList())) ? 1 : 0;
            } catch (Exception ignored) {
                if(except == 1)
                    throw ignored;
                else
                    return 0;
            }
        }).sum()/(double)cartProd.size();
    }


    public static double evaluateWithExamples(int except, Evaluator evaluator, List<List<grt.MathExpression>> examples) {
        return (double)examples.stream().mapToInt(x -> {
            try {
                return evaluator.apply(x.stream().map(
                        y -> y.accept(copyVisitor)).collect(Collectors.toList()),
                        x.stream().map(y -> y.accept(convertToHw1Visitor)).collect(Collectors.toList())) ? 1 : 0;
            } catch (Exception ignored) {
                if(except == 1)
                    throw ignored;
                else
                    return 0;
            }
        }).sum()/(double)examples.size();
    }

    public static double evaluateWithExamples(int except, DocEvaluator evaluator, List<List<grt.DocElement>> examples) {
        return (double)examples.stream().mapToInt(x -> {
            try {
                return evaluator.apply(x.stream().map(
                        y -> y.accept(copyDocVisitor)).collect(Collectors.toList()),
                        x.stream().map(y -> y.accept(convertToHw1DocVisitor)).collect(Collectors.toList())) ? 1 : 0;
            } catch (Exception ignored) {
                if(except == 1)
                    throw ignored;
                else
                    return 0;
            }
        }).sum()/(double)examples.size();
    }

    public static double evaluateWithExamples(int except, DocEvaluator evaluator, List<grt.DocElement>... examples) {
        List<List<grt.DocElement>> cartProd = Lists.cartesianProduct(examples);
        return (double)cartProd.stream().mapToInt(x -> {
            try {
                return evaluator.apply(x.stream().map(
                        y -> y.accept(copyDocVisitor)).collect(Collectors.toList()),
                        x.stream().map(y -> y.accept(convertToHw1DocVisitor)).collect(Collectors.toList())) ? 1 : 0;
            } catch (Exception ignored) {
                if(except == 1)
                    throw ignored;
                else
                    return 0;
            }
        }).sum()/(double)cartProd.size();
    }
}
