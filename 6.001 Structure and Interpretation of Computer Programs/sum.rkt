#lang racket
(define (sum term a next b)
  (if (> a b) 0
      (+ (term a) (sum term (next a) next b))))

(define (inc n) (+ n 1))

(define (sum-cubes a b)
  (sum cube a inc b))

(define (cube x) (* x x x))

(sum-cubes 1 10)

(define (identity x) x)

(define (sum-integers a b)
  (sum identity a inc b))
(sum-integers 1 10)

(define (pi-sum a b)
  (define (pi-term x)
    (/ 1.0 (* x (+ x 2))))
  (define (pi-next x)
    (+ x 4))
  (sum pi-term a pi-next b))
(* 8 (pi-sum 1 1000))

(define (simpson f a b n)
  (define h (/ (- b a) n))
  (define a0 a)
  (define b0 b)
  (define (simpson-term x)
    (cond ((or (= x a0) (= x b0)) (f x))
          ((= (remainder (/ (- x a0) h) 2) 1) (* 4 (f x)))
          ((= (remainder (/ (- x a0) h) 2) 0) (* 2 (f x)))))
  (define (simpson-next a)
    (+ a h))
  (* (sum simpson-term a simpson-next b) (/ h 3)))


(define (sum-iter term a next b)
  (define (iter a result)
    (if (> a b)
        result
        (iter (next a) (+ result (term a)))))
  (iter a 0))
(simpson cube 1 2 1000)

