# Items, Expressions, and Data Mapping

## Learning objectives

By the end of this lesson, you can:

- explain n8n's item-oriented data structure;
- reference current and previous node data without hard-coded copies;
- choose expressions for field-level computation and Code/Edit Fields for transformations;
- avoid item-linking and type-conversion errors.

## Items are the execution unit

Most nodes exchange an array of items. Each item contains a json object and may contain binary data. Conceptually:

~~~json
[
  {"json": {"case_id": "C-001", "amount": 42.5}},
  {"json": {"case_id": "C-002", "amount": 10.0}}
]
~~~

A node normally runs once per item or operates on all items according to its configuration. Inspect the node documentation; assuming one mode can silently create wrong totals or repeated API calls.

## Expressions reference execution data

An expression parameter is evaluated during execution. The editor can create references by dragging data from the input panel. Common concepts include:

- current item's JSON fields;
- data from a named earlier node;
- current timestamp and execution context;
- small transformations supported by the expression runtime.

Prefer the current input when possible. Reaching far back to a named node couples the workflow to topology and item pairing. If a field is needed later, shape it into a clear intermediate contract.

## Expression or transformation node?

- Use an **expression** for a parameter derived from the current item.
- Use **Edit Fields** to select, rename, remove, or add explicit fields.
- Use **Code** for nontrivial deterministic transformation that is clearer in JavaScript.
- Use purpose-built nodes for sorting, aggregating, splitting, or merging when their semantics fit.

Do not place secrets into expressions that become execution data. Use credentials. Validate types explicitly because a numeric-looking string and a number behave differently.

## Item linking

n8n tracks which output item came from which input item so later expressions can resolve the corresponding data. Linking becomes important when Code nodes create, remove, or reorder items or when branches merge. Prefer operations that preserve one-to-one correspondence; when writing Code, follow the official item-linking rules.

## Free local practice

1. Extend the first workflow to create four items with case_id, unit_price, quantity, and owner.
2. Use Edit Fields and expressions to calculate subtotal and a normalized owner value.
3. Add a tax rate field to an earlier Configuration node and reference it in the calculation.
4. Filter out nonpositive quantities with an explicit rejection reason.
5. Use a Code node to return a new record for each valid item with:

~~~javascript
return $input.all().map((item, index) => ({
  json: {
    ...item.json,
    line_number: index + 1,
    total: Number(item.json.unit_price) * Number(item.json.quantity),
  },
  pairedItem: { item: index },
}));
~~~

6. Reorder or filter the inputs and verify each output still maps to the correct case.
7. Test quantity as 2, "2", 0, missing, and "two." Route invalid types rather than producing NaN.
8. Remove unnecessary source fields from the final contract while retaining a case ID.

## Completion criteria

You are finished when:

- you can identify the array, item, json, and field levels in node output;
- derived values come from expressions or explicit transformation, not pasted copies;
- numeric strings, missing values, zero, and invalid text have defined behavior;
- every output retains a correlation identifier;
- the Code node returns the documented n8n item structure;
- filtering or reordering does not associate data with the wrong case;
- secret or sensitive body data is absent from configuration and logs.

## References

- [n8n documentation: Data structure](https://docs.n8n.io/data/data-structure/) - official item, JSON, and binary-data model.
- [n8n documentation: Expressions](https://docs.n8n.io/code/expressions/) - official expression syntax and available context.
- [n8n documentation: Referencing data in the UI](https://docs.n8n.io/data/data-mapping/data-mapping-ui/) - official drag-and-drop and expression mapping guidance.
- [n8n documentation: Item linking](https://docs.n8n.io/data/data-mapping/data-item-linking/) - official explanation of correspondence between input and output items.
