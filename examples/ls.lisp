; An example plist program that prints all files in the current working directory
; This program demonstrates several plisp constructs as well as basic python interop

(define os (import "os"))
(define getcwd (. os "getcwd"))
(define listdir (. os "listdir"))

(fn print_list (ls) 
    (if
      ls 
      (do 
        (print (first ls)) 
        (print_list (rest ls)))
      nil))

(print_list (! listdir (! getcwd)))
