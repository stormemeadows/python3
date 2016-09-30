# Author: storm

class ModuloCalculator(object):
    """
    This class keeps modular calculations' time- and space-complexities
        linear and constant, resp.

    Python has built-in support for unlimited precision integers, so
        this class isn't necessary for many scenarios requiring modular
        arithmetic (you can often just save the modulo operation until the end).
        That would be too easy though, and not possible in most languages
            without using external libraries.
        This class is easily translated into other languages without requiring
            special support for numbers large enough to cause an overflow.

    IMPORTANT:
        Watch out for zero-divisors! (a bit on ring theory)
        Not a problem if your modulus is prime though, since that would
            mean you're working with a finite field and hence an integral
            domain. Integral domains don't have zero-divisors, by definition.
    """

    def __init__(self, modulus):
        super(ModuloCalculator, self).__init__()
        self.__set_mod(modulus)


    def __del__(self):
    #     print(" ** %s is dying **"%str(self))
        del self.mod
    #     print("max fact call:         ",self._max_call_to_factorial)
        del self._max_call_to_factorial
    #     print("unique fact calls:     ",len(self._prev_factorial_calculations))
        del self._prev_factorial_calculations
    #     print("unique inv fact calls: ",len(self._prev_inverse_factorial_calculations))
        del self._prev_inverse_factorial_calculations
    #     print(" ** %s is dead **\n"%str(self))


    @staticmethod
    def modulo_inverse(
            m: dict(type=int, help='a prime, otherwise n may not have an inverse'),
            n: dict(type=int, help='any positive integer')
        ) ->   dict(type=int, help='(n mod m)^-1'):
        """
        NOTE: Watch out for zero-divisors! (a bit on ring theory)
              Not a problem if your modulus is prime though, since that
              would  mean you're working with a finite field and hence an integral
              domain; integral domains don't have zero-divisors, by definition.
        """

        ## If our m is prime, we don't need this line:
        # if n%m == 0: return 0

        t, t2 = 0, 1
        r, r2 = m, n
        f = lambda x,x2,q: [x2, x - x2 * q]
        while r2 != 0:
            q     = r // r2
            t, t2 = f(t,t2,q)
            r, r2 = f(r,r2,q)

        ## If our m is prime, we don't need this line either:
        # if r > 1: raise "(%d mod %d)^-1 does not exist!"%(n,m)
        return t if t<1 else t+m



    def multiplicative_inverse(self,n):
        return ModuloCalculator.modulo_inverse(self.mod,n)



    def multiply(self,n,k):
        m = self.mod
        return ((n%m) * (k%m))%m
        # return n*k%self.mod



    def add(self,n,k):
        m = self.mod
        return ((n%m) + (k%m))%m
        # return (n+k)%self.mod



    def divide(self,n:"dividend",k:"divisor"):
        return self.multiply(n, multiplicative_inverse(k))



    def __set_mod(self, mod):
        self.mod = mod
        self._max_call_to_factorial = 1
        self._prev_inverse_factorial_calculations = {}
        self._prev_factorial_calculations         = {1:1} #base case
                                                          #(we don't need {0:1})



    def _get_max_computed_factorial(self):
        return self._prev_factorial_calculations[self._max_call_to_factorial]



    def mod_fact(self,n_in):
        """
        The factorial function, with a few performance tweaks:
            - No recursion
            - Nothing is calculated more than once
        """
        n = n_in%self.mod

        k = self._max_call_to_factorial
        if n <= k:  # if n <= 1: return 1
            return self._prev_factorial_calculations[n]


        # An iterative implementation, starting with
        #   our greatest previous call.
        prod = self._prev_factorial_calculations[k]
        for i in range(k+1, n+1):
            prod = self.multiply(prod,i)  #= (prod * i) % self.mod
            self._prev_factorial_calculations[i] = prod
            self._max_call_to_factorial = i

        return prod



    def mod_inverse_fact(self,n):
        if n in self._prev_inverse_factorial_calculations:
            return self._prev_inverse_factorial_calculations[n]

        inv_prod = self.multiplicative_inverse(self.mod_fact(n))
        self._prev_inverse_factorial_calculations[n] = inv_prod
        return inv_prod

