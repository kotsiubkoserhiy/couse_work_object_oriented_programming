import time

class LinearInterpolation:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.iterations = 0
        self.operations = 0
        self.execution_time = 0.0


    def interpolate(self, x_point):
        start_time = time.time()
        n = len(self.x)
        i = 0

        if self.x[0] == x_point:
            y_result = self.y[0]
        elif x_point > self.x[n-1]:
            y_result = self.y[n-1]
        else:
            for i in range(n-1):
                self.iterations +=1
                if self.x[i] < x_point <= self.x[i+1]:
                    y_result = self.y[i] + (self.y[i+1] - self.y[i]) * (x_point - self.x[i]) / (self.x[i+1] - self.x[i])
                    self.operations += 6
        
        self.execution_time = time.time() - start_time
        return y_result
    
    def print_polynomial(self):
        n = len(self.x)
        polinoms = ''
        for i in range(n - 1):
            polinoms += ("Polynomial between x[{0}]={1} and x[{2}]={3}:\n".format(i, self.x[i], i+1, self.x[i+1]))
            polinoms += ("y = {0} + ({1} - {0}) * (x - {2}) / ({3} - {2})\n".format(self.y[i], self.y[i+1], self.x[i], self.x[i+1]))
        polinoms += '\n'
        return polinoms


class CubicSpline:
    class SplineTuple:
        def __init__(self, x, a):
            self.x = x
            self.a = a
            self.c = 0.
            self.b = 0.
            self.d = 0.

    def __init__(self):
        self.splines = None
        self.n = 0
        self.iterations = 0
        self.operations = 0
        self.execution_time = 0.0
        self.start_time = time.time()

    def build_spline(self, x, y):
        
        self.n = len(x)

        # Ініціалізація масиву сплайнів
        self.splines = [CubicSpline.SplineTuple(x[i], y[i]) for i in range(self.n)]
        self.splines[0].c = self.splines[self.n - 1].c = 0.

        # Рішення СЛАР щодо коефіцієнтів сплайнів c[i] методом прогонки для трьохіагональних матриць
        # Обчислення прогоночних коефіцієнтів - прямий хід методу прогонки
        alpha = [0.0] * (self.n - 1)
        beta = [0.0] * (self.n - 1)
        A, B, C, F, h_i, h_i1, z = (0.0,) * 7
        alpha[0] = beta[0] = 0.

        for i in range(1, self.n-1):
            self.iterations += 1
            h_i = x[i] - x[i - 1]
            h_i1 = x[i + 1] - x[i]
            A = h_i
            C = 2. * (h_i + h_i1)
            B = h_i1
            F = 6. * ((y[i + 1] - y[i]) / h_i1 - (y[i] - y[i - 1]) / h_i)
            z = (A * alpha[i - 1] + C)
            alpha[i] = -B / z
            beta[i] = (F - A * beta[i - 1]) / z
            self.operations += 14

            # Обчислення коренів рівнянь сплайнів методом зворотнього ходу методу прогонки
        #self.splines[self.n-1].c = (F-A*beta[self.n-2])/(C+A*alpha[self.n-2])
        i = self.n - 2
        while i > 0:
            self.iterations += 1
            self.splines[i].c = alpha[i] * self.splines[i + 1].c + beta[i]
            i -= 1
            self.iterations += 1

        # Обчислення значень b[i] та d[i]
        for i in range(self.n - 1, 0, -1):
            self.iterations += 1
            h_i = x[i] - x[i - 1]
            self.splines[i].d = (self.splines[i].c - self.splines[i - 1].c) / h_i
            self.splines[i].b = h_i * (2. * self.splines[i].c + self.splines[i - 1].c) / 6. + (y[i] - y[i - 1]) / h_i
            self.operations += 9

    def interpolate(self, x_point):
        if not self.splines:
            return None

        s = None

        # Пошук відповідного сплайну для інтерполяції
        if x_point <= self.splines[0].x:
            s = self.splines[0]
            self.iterations += 1
        elif x_point >= self.splines[self.n - 1].x:
            s = self.splines[self.n - 1]
            self.iterations += 1
        else:
            i = 0
            j = self.n - 1
            while i + 1 < j:
                self.iterations += 1
                k = i + (j - i) // 2
                if x_point <= self.splines[k].x:
                    j = k
                else:
                    i = k

            s = self.splines[j]

        # Обчислення значення інтерпольованої функції
        dx = x_point - s.x
        result = s.a + (s.b + (s.c / 2. + s.d * dx / 6.) * dx) * dx
        self.operations += 9
        
        self.execution_time = time.time() - self.start_time
        
        return result
    
    def print_polynomial(self):
        if not self.splines:
            return
        polinoms = ''
        for i in range(self.n - 1):
            polinoms += ("Polynomial between x[{0}]={1} and x[{2}]={3}:\n".format(i, self.splines[i].x, i + 1, self.splines[i + 1].x))
            polinoms += ("f(x) = {0:.3f} + {1:.3f}(x - {2:.3f}) + {3:.3f}(x - {2:.3f})^2 + {4:.3f}(x - {2:.3f})^3\n".format(self.splines[i].a, self.splines[i].b, self.splines[i].x, self.splines[i].c, self.splines[i].d))
        polinoms +='\n'
        return polinoms
        
        