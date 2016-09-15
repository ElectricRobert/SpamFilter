 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 ~                        Ham/Spam Naive Bayesian Classifier 
 ~						   created by: Robert Herrera
 ~
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. ----------------------------------------------------------------------------------------------
NOTE: The necessary files to evaluate the necessary evalution1 and evaluation2 idx files 
have been pre computed and stored as evaluation1_output.txt and evaluation2_output.txt .If you wish to re-evaluate from scratch, please
refer to evalution(4)

2. ----------------------------------------------------------------------------------------------

The default dictionary output of the spam filter program is in dictionary.txt. This file is necessary
when using the evaluation program. 

3. ----------------------------------------------------------------------------------------------
 expample script to invoke training program:
 python train.py --corpus ./trec05p-1/ --key_file ./CompanionFiles2/train.key --train_file ./CompanionFiles2/train.idx 

4. ----------------------------------------------------------------------------------------------
 example script to invoke evaluation program:
 python evaluation.py --file ./CompanionFiles2/test1.idx --corpus ./trec05p-1/ -d dictionary.txt --output output.txt

  - for example if you were to perform an evaluatin on evaluation.idx, invoke the following:
  	python evaluation.py --file ./CompanionFiles2/evaluation1.idx --corpus ./trec05p-1/ -d dictionary.txt --output eval_output.txt
5. ----------------------------------------------------------------------------------------------

 example script to invoke compute performance program:
 python compute_performance.py --test output.key --target ./CompanionFiles2/test1.key 

 - for exmpale is you were to perform a test performance on a secret, unknown evaluation.key you would type the following:

  	python compute_performance.py --test output.key --target ./Absolute/Path/To/Secret/Key/evaluation.key

  										or

  	python compute_performance.py --test output.key --target /Users/PDeleon/Absolute/Path/To/Secret/Key/evaluation.key