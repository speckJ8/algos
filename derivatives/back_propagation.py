"""
Edges represent values
Nodes represent operations

---- (a) -----> [+] --- (a + b) -->
                 ^
                 |
----- (b) --------

"""

from dataclasses import dataclass


class Op:
    """
    A generalized computation, i.e., a node in the computational graph
    """
    name: str

    def run(self, context: Context):
        pass

    def grad(self, var: str, context: Context):
        pass


class AddOp(Op):
    def __init__(self, left: str, right: str, name: str):
        super().__init__()
        self.name = name
        self._left = left
        self._right = right

    def run(self, context: Context):
        l = context.values[self._left]
        r = context.values[self._right]
        context.values[self.name] = l + r
        context.gradients[(self.name, self._left)] = 1
        context.gradients[(self.name, self._right)] = 1

    def grad(self, var: str, context: Context):
        context.gradients[(self.name, var)] = (
            context.gradients.get((self._left, var), 0) + context.gradients.get((self._right, var), 0)
        )

class MulOp(Op):
    def __init__(self, left: str, right: str, name: str):
        super().__init__()
        self.name = name
        self._left = left
        self._right = right

    def run(self, context: Context) -> float:
        l = context.values[self._left]
        r = context.values[self._right]
        context.values[self.name] = l * r
        context.gradients[(self.name, self._left)] = r
        context.gradients[(self.name, self._right)] = l

    def grad(self, var: str, context: Context):
        context.gradients[(self.name, var)] = (
            context.gradients[(self.name, self._left)] * context.gradients.get((self._left, var), 0) +
            context.gradients[(self.name, self._right)] * context.gradients.get((self._right, var), 0)
        )


@dataclass
class Context:
    values: dict[str, float]
    gradients: dict[(str, str), float]


class ComputationalGraph:
    def __init__(self, layers: list[list[Op]]):
        self._layers = layers
        self._ops: dict[str, Op] = {}
        for layer in layers:
            for op in layer:
                self._ops[op.name] = op
    
    def run(self, values: dict[str, float]) -> Context:
        initial_gradients = {(k, k): 1 for k, _ in values.items()}
        context = Context(values=values, gradients=initial_gradients)
        for layer in self._layers:
            for op in layer:
                op.run(context)
        return context

    def grad(self, var: str, values: dict[str, float]) -> Context:
        context = self.run(values)
        for layer in self._layers:
            for op in layer:
                op.grad(var, context)
        return context
