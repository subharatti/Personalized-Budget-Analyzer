import { useEffect, useState } from "react";
import { View, Text, StyleSheet, ScrollView, TextInput, Pressable } from "react-native";

const API_URL = "http://localhost:5000";

export default function HomeScreen() {
  const [expenses, setExpenses] = useState<Record<string, number>>({});
  const [income, setIncome] = useState<number>(0);

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API_URL}/api/summary`)
      .then((res) => res.json())
      .then((data) => {
        setExpenses(data.expenses);
        setIncome(data.income);
        setError("");
      })
      .catch(() => {
        setError("Failed to load data from backend.");
      });
  }, []);

  function askQuestion() {
    if (!question.trim()) return;

    setLoading(true);
    setAnswer("");
    setError("");

    fetch(`${API_URL}/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    })
      .then((res) => res.json())
      .then((data) => {
        setAnswer(data.answer || "No answer returned.");
      })
      .catch(() => {
        setError("Something went wrong while asking the question.");
      })
      .finally(() => {
        setLoading(false);
      });
  }

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Budget Overview</Text>

      {error !== "" && <Text style={styles.error}>{error}</Text>}

      <View style={styles.card}>
        {Object.keys(expenses).length === 0 && !error && (
          <Text>No spending data available.</Text>
        )}

        {Object.entries(expenses).map(([category, amount]) => (
          <Text key={category} style={styles.row}>
            {category}: ${amount.toFixed(2)}
          </Text>
        ))}

        <Text style={styles.income}>
          Total Income: ${income.toFixed(2)}
        </Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.subtitle}>Ask About Your Spending</Text>

        <TextInput
          style={styles.input}
          placeholder="Why did my spending increase this month?"
          value={question}
          onChangeText={setQuestion}
        />

        <Pressable
          style={[styles.button, loading && styles.buttonDisabled]}
          onPress={askQuestion}
          disabled={loading}
        >
          <Text style={styles.buttonText}>
            {loading ? "Thinking..." : "Ask"}
          </Text>
        </Pressable>

        {answer !== "" && <Text style={styles.answer}>{answer}</Text>}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: "#f6fbf6",
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    color: "#1f7a1f",
    marginBottom: 20,
  },
  subtitle: {
    fontSize: 18,
    fontWeight: "600",
    marginBottom: 12,
    color: "#1f7a1f",
  },
  card: {
    backgroundColor: "white",
    padding: 16,
    borderRadius: 12,
    marginBottom: 20,
  },
  row: {
    fontSize: 16,
    marginBottom: 4,
  },
  income: {
    marginTop: 10,
    fontWeight: "bold",
    color: "#3fa34d",
  },
  input: {
    borderWidth: 1,
    borderColor: "#ccc",
    borderRadius: 8,
    padding: 12,
    marginBottom: 10,
  },
  button: {
    backgroundColor: "#2e7d32",
    padding: 12,
    borderRadius: 8,
    alignItems: "center",
  },
  buttonDisabled: {
    backgroundColor: "#a5d6a7",
  },
  buttonText: {
    color: "white",
    fontWeight: "bold",
  },
  answer: {
    marginTop: 10,
    fontSize: 15,
    lineHeight: 20,
  },
  error: {
    color: "red",
    marginBottom: 10,
  },
});
