package hw1;

import com.google.common.collect.Lists;
import com.google.common.collect.Streams;
import grt.Num;
import grt.Op;
import org.json.simple.JSONObject;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.function.Predicate;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import static hw1.ComparatorUtils.*;
import static hw1.ExampleUtils.*;

public class MainTester {

    public static JSONObject json = new JSONObject();

    public static boolean basic_getter_test(List<grt.MathExpression> grt, List<hw1.MathExpression> hw1) {
        return cmpExps(hw1.get(0),grt.get(0));
    }


    public static boolean match_test(List<grt.MathExpression> grt, List<hw1.MathExpression> hw1) {
        boolean grt_result = grt.get(0).match(grt.get(1));
        boolean hw1_result = hw1.get(0).match(hw1.get(1));
        return cmpExps(hw1.get(0),grt.get(0)) && grt_result == hw1_result;
    }

    public static boolean double_match_test(List<grt.MathExpression> grt, List<hw1.MathExpression> hw1) {
        boolean grt_result = grt.get(0).match(grt.get(1));
        boolean hw1_result = hw1.get(0).match(hw1.get(1));
        boolean grt_result2 = grt.get(0).match(grt.get(2));
        boolean hw1_result2 = hw1.get(0).match(hw1.get(2));
        return cmpExps(hw1.get(0),grt.get(0)) && grt_result == hw1_result && grt_result2 == hw1_result2;
    }


    public static boolean countAtomicsVisitor_test(List<grt.MathExpression> grt, List<hw1.MathExpression> hw1)
    {
        int num = hw1.get(0).accept(new hw1.CountAtomicsVisitor());
        return grt.get(0).accept(countAtomicsVisitor) ==  num ||
                grt.get(0).accept(countAtomicsVisitor2) == num;
    }

    public static boolean clearVarsVisitor_test(List<grt.MathExpression> grt, List<hw1.MathExpression> hw1) {
        grt.get(0).accept(clearVarsVisitor);
        hw1.get(0).accept(new hw1.ClearVarsVisitor());
        return cmpExps(hw1.get(0), grt.get(0));
    }

    public static boolean printMathVisitor_test(List<grt.MathExpression> grt, List<hw1.MathExpression> hw1) {
        return cmpPrintMath(hw1.get(0),grt.get(0));
    }

    public static boolean rule_test(grt.Rule rule, hw1.Rule hw1rule, grt.MathExpression grt, hw1.MathExpression hw1)
    {
        boolean before_match = cmpExps(hw1rule.getPremise(), rule.getPremise()) && cmpExps(hw1rule.getEntails(),
                rule.getEntails());
        boolean hw1apply = hw1rule.apply(hw1);
        boolean grtapply = rule.apply(grt);
        boolean premise_after_match = cmpExps(hw1rule.getPremise(),rule.getPremise());
        boolean entails_after_match = cmpExps(hw1rule.getEntails(), rule.getEntails());
        rule.clear();
        hw1rule.clear();
        boolean clear_match = cmpExps(hw1rule.getPremise(), rule.getPremise()) &&
                cmpExps(hw1rule.getEntails(), rule.getEntails());
        return before_match && hw1apply == grtapply && premise_after_match && entails_after_match && clear_match;
    }

    public static boolean XDotYDivX_test(List<grt.MathExpression> grt, List<hw1.MathExpression> hw1) {
        grt.Rule rule = new grt.XDotYDivXIsYRule(new grt.Var(0), new grt.Var(1));
        hw1.Rule hw1rule = new hw1.XDotYDivXIsYRule(new hw1.Var(0), new hw1.Var(1));
        return rule_test(rule, hw1rule, grt.get(0), hw1.get(0));
    }

    public static boolean XDotZero_test(List<grt.MathExpression> grt, List<hw1.MathExpression> hw1) {
        grt.Rule rule = new grt.XDotZeroIsZeroRule(new grt.Var(0));
        hw1.Rule hw1rule = new hw1.XDotZeroIsZeroRule(new hw1.Var(0));
        return rule_test(rule, hw1rule, grt.get(0), hw1.get(0));
    }

    public static boolean XplusX_test(List<grt.MathExpression> grt, List<hw1.MathExpression> hw1) {
        grt.Rule rule = new grt.XPlusXIs2XRule(new grt.Var(0));
        hw1.Rule hw1rule = new hw1.XPlusXIs2XRule(new hw1.Var(0));
        return rule_test(rule, hw1rule, grt.get(0), hw1.get(0));
    }

    public static boolean basic_doc_getter_test(List<grt.DocElement> grt, List<hw1.DocElement> hw1) {
        return cmpDocs(hw1.get(0), grt.get(0));
    }

    public static boolean printHTML_test(List<grt.DocElement> grt, List<hw1.DocElement> hw1) {
        return cmpPrintHTML(hw1.get(0), grt.get(0));
    }

    public static void main(String[] args){

        int except = Integer.parseInt(args[1]);
        int list = Integer.parseInt(args[2]);

        json.put("student_id",Integer.parseInt(args[0]));

        ConvertToHw1Visitor convertToHw1Visitor = new ConvertToHw1Visitor();

        List<grt.MathExpression> basicExamplesWithEmptyVars = Stream.concat(
                basicExamplesWithoutVars.stream(),
                basicEmptyVars.stream()
        ).collect(Collectors.toList());

        List<grt.MathExpression> basicExamplesAll = Stream.concat(
                basicExamplesWithEmptyVars.stream(),
                basicFilledVars.stream()
        ).collect(Collectors.toList());

        List<grt.MathExpression> complexExamplesAll = Stream.concat(
                complexExamplesWithoutVars.stream(),
                complexExamplesWithVars.stream()
        ).collect(Collectors.toList());
        complexExamplesAll.addAll(complexExamplesWithEmptyVars);


        json.put("basic_getter_test", evaluateWithExamples(except, MainTester::basic_getter_test, basicExamplesWithEmptyVars));



        List<List<grt.MathExpression>> trueBasicMatchExamples = Stream.concat(
                Streams.zip(basicExamplesWithoutVars.stream(),
                        basicExamplesWithoutVars.stream(), (x,y) -> List.of(x,y)),
                Streams.zip(basicEmptyVars.stream(),
                        basicExamplesWithoutVars.stream(), (x,y) -> List.of(x,y))
        ).collect(Collectors.toList());

        List<grt.MathExpression> shuffledBasicExamplesWithoutVars = new ArrayList<>(basicExamplesWithoutVars);
        List<grt.MathExpression> shuffledBasicExamplesWithoutVars2 = new ArrayList<>(basicExamplesWithoutVars);
        Collections.shuffle(shuffledBasicExamplesWithoutVars, random);
        Collections.shuffle(shuffledBasicExamplesWithoutVars2, random);

        List<List<grt.MathExpression>> falseBasicMatchExamples = Lists.cartesianProduct(
                shuffledBasicExamplesWithoutVars,
                shuffledBasicExamplesWithoutVars2
        ).stream().filter(x -> x.get(0) != x.get(1)).limit(trueBasicMatchExamples.size()).collect(Collectors.toList());

        List<List<grt.MathExpression>> basicMatchExamples = Stream.concat(
                trueBasicMatchExamples.stream(), falseBasicMatchExamples.stream()).collect(Collectors.toList());

        List<List<grt.MathExpression>> doubleBasicMatchExamples = Lists.cartesianProduct(
                basicMatchExamples,
                basicMatchExamples.stream().map(x -> List.of(x.get(1))).collect(Collectors.toList())
        ).stream().map(x -> Stream.concat(x.get(0).stream(),x.get(1).stream()).collect(Collectors.toList())
        ).collect(Collectors.toList());

        json.put("basic_match_true_test", evaluateWithExamples(except, MainTester::match_test, trueBasicMatchExamples));
        json.put("basic_match_false_test", evaluateWithExamples(except, MainTester::match_test, falseBasicMatchExamples));
        json.put("basic_match_double_true_test", evaluateWithExamples(except, MainTester::double_match_test, doubleBasicMatchExamples));





        List<List<grt.MathExpression>> trueComplexMatchExamples = Streams.concat(
                Streams.zip(complexExamplesWithoutVars.stream(),
                        complexExamplesWithoutVars.stream(), (x,y) -> List.of(x,y)),
                Streams.zip(complexExamplesWithVars.stream(),
                        complexExamplesWithoutVars.stream(), (x,y) -> List.of(x,y)),
                Streams.zip(complexExamplesWithEmptyVars.stream(),
                        complexExamplesWithoutVars.stream(), (x,y) -> List.of(x,y))
        ).collect(Collectors.toList());

        List<grt.MathExpression> shuffledComplexExamplesWithoutVars = new ArrayList<>(complexExamplesWithoutVars);
        List<grt.MathExpression> shuffledComplexExamplesWithoutVars2 = new ArrayList<>(complexExamplesWithoutVars);
        List<grt.MathExpression> shuffledComplexExamplesWithVars = new ArrayList<>(complexExamplesWithVars);
        List<grt.MathExpression> shuffledComplexExamplesWithEmptyVars = new ArrayList<>(complexExamplesWithEmptyVars);
        Collections.shuffle(shuffledComplexExamplesWithoutVars, random);
        Collections.shuffle(shuffledComplexExamplesWithVars, random);
        Collections.shuffle(shuffledComplexExamplesWithEmptyVars, random);
        Collections.shuffle(shuffledBasicExamplesWithoutVars2, random);

        Predicate<List<grt.MathExpression>> does_not_match = x ->
                !(x.get(0).accept(copyVisitor)).match(x.get(1).accept(copyVisitor));

        List<List<grt.MathExpression>> falseComplexMatchExamples = Lists.cartesianProduct(
                Streams.concat(
                        shuffledComplexExamplesWithoutVars.stream(),
                        shuffledComplexExamplesWithVars.stream(),
                        shuffledComplexExamplesWithEmptyVars.stream()
                ).collect(Collectors.toList()),
                shuffledBasicExamplesWithoutVars2
        ).stream().filter(does_not_match).limit(trueComplexMatchExamples.size()).collect(Collectors.toList());

        List<List<grt.MathExpression>> complexMatchExamples = Stream.concat(
                trueComplexMatchExamples.stream(), falseComplexMatchExamples.stream()).collect(Collectors.toList());

        List<List<grt.MathExpression>> doubleComplexMatchExamples = Lists.cartesianProduct(
                complexMatchExamples,
                complexMatchExamples.stream().map(x -> List.of(x.get(1))).collect(Collectors.toList())
        ).stream().map(x -> Stream.concat(x.get(0).stream(),x.get(1).stream()).collect(Collectors.toList())
        ).collect(Collectors.toList());

        json.put("complex_match_true_test", evaluateWithExamples(except, MainTester::match_test, trueComplexMatchExamples));
        json.put("complex_match_false_test", evaluateWithExamples(except, MainTester::match_test, falseComplexMatchExamples));
        json.put("complex_match_double_test", evaluateWithExamples(except, MainTester::double_match_test, doubleComplexMatchExamples));

        json.put("basic_clear_vars_test", evaluateWithExamples(except, MainTester::clearVarsVisitor_test, basicExamplesAll));

        json.put("complex_clear_vars_test", evaluateWithExamples(except, MainTester::clearVarsVisitor_test, complexExamplesAll));

        json.put("basic_count_atomics_test",evaluateWithExamples(except, MainTester::countAtomicsVisitor_test, basicExamplesAll));

        json.put("complex_count_atomics_test",evaluateWithExamples(except, MainTester::countAtomicsVisitor_test, complexExamplesAll));

        json.put("basic_print_math_test", evaluateWithExamples(except, MainTester::printMathVisitor_test, basicExamplesAll));

        json.put("complex_print_math_test", evaluateWithExamples(except, MainTester::printMathVisitor_test, complexExamplesAll));

        List<List<grt.MathExpression>> trueBasicXdotXExamples = Lists.cartesianProduct(
                basicExamplesWithoutVars,
                shuffledBasicExamplesWithoutVars
        ).stream().map(x ->
        {
            grt.MathExpression dot = new grt.Op("*", x.get(0), x.get(1));
            grt.MathExpression div = new grt.Op("/", dot, x.get(0));
            return List.of(div);
        }).collect(Collectors.toList());

        List<List<grt.MathExpression>> falseBasicXdotXExamples = Lists.cartesianProduct(
                shuffledBasicExamplesWithoutVars,
                shuffledBasicExamplesWithoutVars2,
                basicExamplesWithoutVars
        ).stream().map(x ->
        {
            grt.MathExpression dot = new grt.Op("*", x.get(0), x.get(2));
            grt.MathExpression div = new grt.Op("/", dot, x.get(1));
            return List.of(div);
        }).limit(trueBasicXdotXExamples.size()).collect(Collectors.toList());

        List<List<grt.MathExpression>> basicXdotXExamples = Streams.concat(
                trueBasicXdotXExamples.stream(),
                falseBasicXdotXExamples.stream(),
                basicExamplesWithoutVars.stream().map(x -> List.of(x))).collect(Collectors.toList());

        json.put("basic_XdotYdivX_test", evaluateWithExamples(except, MainTester::XDotYDivX_test, basicXdotXExamples));

        List<List<grt.MathExpression>> trueComplexXdotXExamples = Lists.cartesianProduct(
                complexExamplesWithoutVars,
                shuffledComplexExamplesWithoutVars
        ).stream().map(x ->
        {
            grt.MathExpression dot = new grt.Op("*", x.get(0), x.get(1));
            grt.MathExpression div = new grt.Op("/", dot, x.get(0));
            return List.of(div);
        }).collect(Collectors.toList());

        List<List<grt.MathExpression>> falseComplexXdotXExamples = Lists.cartesianProduct(
                shuffledComplexExamplesWithoutVars,
                shuffledComplexExamplesWithoutVars2,
                complexExamplesWithoutVars
        ).stream().map(x ->
        {
            grt.MathExpression dot = new grt.Op("*", x.get(0), x.get(2));
            grt.MathExpression div = new grt.Op("/", dot, x.get(1));
            return List.of(div);
        }).limit(trueComplexXdotXExamples.size()).collect(Collectors.toList());

        List<List<grt.MathExpression>> complexXdotXExamples = Streams.concat(
                trueComplexXdotXExamples.stream(),
                falseComplexXdotXExamples.stream(),
                complexExamplesWithoutVars.stream().map(x -> List.of(x))).collect(Collectors.toList());

        json.put("complex_XdotYdivX_test", evaluateWithExamples(except, MainTester::XDotYDivX_test, complexXdotXExamples));


        List<List<grt.MathExpression>> basicDotZero = basicExamplesWithoutVars.stream().map(
                x -> List.of( (grt.MathExpression)(new grt.Op("*", x, new grt.Num(0))))
        ).collect(Collectors.toList());

        List<List<grt.MathExpression>> complexDotZero = complexExamplesWithoutVars.stream().map(
                x -> List.of( (grt.MathExpression)(new grt.Op("*", x, new Num(0))))
        ).collect(Collectors.toList());

        basicDotZero = Streams.concat(basicDotZero.stream(),
                        basicExamplesWithoutVars.stream().map(x -> List.of(x))
                ).collect(Collectors.toList());

        complexDotZero = Streams.concat(complexDotZero.stream(),
                complexExamplesWithoutVars.stream().map(x -> List.of(x))
        ).collect(Collectors.toList());

        json.put("basic_XdotZero_test", evaluateWithExamples(except, MainTester::XDotZero_test, basicDotZero));
        json.put("complex_XdotZero_test", evaluateWithExamples(except, MainTester::XDotZero_test, complexDotZero));

        List<List<grt.MathExpression>> basicXplusXTrue = basicExamplesWithoutVars.stream().map(
                x -> List.of( (grt.MathExpression)(new grt.Op("+", x, x)))
        ).collect(Collectors.toList());

        List<List<grt.MathExpression>> basicXplusXFalse = Lists.cartesianProduct(
                shuffledBasicExamplesWithoutVars,
                shuffledBasicExamplesWithoutVars2
                ).stream().filter(x -> x.get(0) != x.get(1)).limit(basicXplusXTrue.size()).map(
                x -> List.of( (grt.MathExpression)(new grt.Op("+", x.get(0), x.get(1))))
        ).collect(Collectors.toList());

        List<List<grt.MathExpression>> basicXplusXExamples = Streams.concat(
                basicXplusXTrue.stream(),
                basicXplusXFalse.stream(),
                basicExamplesWithoutVars.stream().map(x -> List.of(x))
        ).collect(Collectors.toList());

        json.put("basic_XplusX_test", evaluateWithExamples(except, MainTester::XplusX_test,basicXplusXExamples));

        List<List<grt.MathExpression>> complexXplusXTrue = complexExamplesWithoutVars.stream().map(
                x -> List.of( (grt.MathExpression)(new grt.Op("+", x, x)))
        ).collect(Collectors.toList());

        List<List<grt.MathExpression>> complexXplusXFalse = Lists.cartesianProduct(
                shuffledComplexExamplesWithoutVars,
                shuffledComplexExamplesWithoutVars2
        ).stream().filter(x -> x.get(0) != x.get(1)).limit(complexXplusXTrue.size()).map(
                x -> List.of( (grt.MathExpression)(new Op("+", x.get(0), x.get(1))))
        ).collect(Collectors.toList());

        List<List<grt.MathExpression>> complexXplusXExamples = Streams.concat(
                complexXplusXTrue.stream(),
                complexXplusXFalse.stream(),
                complexExamplesWithoutVars.stream().map(x -> List.of(x))
        ).collect(Collectors.toList());

        json.put("complex_XplusX_test", evaluateWithExamples(except, MainTester::XplusX_test,complexXplusXExamples));

        json.put("basic_doc_getter_test", evaluateWithExamples(except, MainTester::basic_doc_getter_test, basicDocuments));

        json.put("basic_printHTML_test", evaluateWithExamples(except, MainTester::printHTML_test, basicDocuments));
        json.put("complex_printHTML_test", evaluateWithExamples(except, MainTester::printHTML_test, complexDocuments));

        if(list == 1) {
            for (Iterator iterator = json.keySet().iterator(); iterator.hasNext(); ) {
                String key = (String) iterator.next();
                if(key.equals("student_id"))
                    System.out.printf("%s : %d\n", key, json.get(key));
                else
                    System.out.printf("%s : %f\n", key, json.get(key));
            }
        }
        else{
            System.out.println(json.toJSONString());
        }




    }
}
