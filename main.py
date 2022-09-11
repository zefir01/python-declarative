from typing import Optional

import declarative


class Parent(declarative.Module):

    @declarative.resource
    def c1(self):
        return """\
        ---
        apiVersion: v1
        kind: Service
        metadata:
          generateName: service-
        spec:
          selector:
            app.kubernetes.io/name: MyApp
          ports:
            - protocol: TCP
              port: 82
              targetPort: 9376
        ---
        apiVersion: v1
        kind: Service
        metadata:
          generateName: service-
        spec:
          selector:
            app.kubernetes.io/name: MyApp
          ports:
            - protocol: TCP
              port: 83
              targetPort: 9376
        ---
        """

    @declarative.resource
    def c2b(self, prev: Optional[str]):
        res = f"""
        apiVersion: v1
        kind: Service
        metadata:
          generateName: service-
        spec:
          selector:
            app.kubernetes.io/name: MyApp
          ports:
            - protocol: TCP
              port: {self.c1.obj[0].spec.ports[0].port}
              targetPort: 9376
        """
        return res

    @declarative.resource
    # @declarative.resource_pass_errors
    def c2(self, prev: Optional[str]):
        # raise Exception("Custom error")
        s = """
        apiVersion: v1
        kind: Service
        metadata:
          generateName: service-
        spec:
          selector:
            app.kubernetes.io/name: MyApp
          ports:
            - protocol: TCP
              port: 81
              targetPort: 9376
        """
        s1 = """
                apiVersion: v1
                kind: Service
                metadata:
                  generateName: service-
                spec:
                  selector:
                    app.kubernetes.io/name: MyApp
                  ports:
                    - protocol: TCP
                      port: 81
                      targetPort: 9376
                """
        return [s, s1]


class Root(declarative.Module):
    @declarative.resource
    def m1(self, prev: Optional[str]):
        # raise Exception("Custom error")
        child1 = Parent()
        child2 = Parent()
        return [child1, child2]


root = Root("Root")
root.init()

print("\nCreated:")
for r in root.get_resources():
    print(r.name)

print("\nErrors:")
for e in root.get_errors():
    print(e.name, e.error)
