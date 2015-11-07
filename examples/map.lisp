; An example implementation and use of a map function

(fn map (f seq)
    (if seq
      (cons (f (first seq)) (map f (rest seq)))
      nil))

(fn plusone (x) (+ 1 x))

(define l '(1 2 3))
(define l2 (map plusone l))
(print l2)
